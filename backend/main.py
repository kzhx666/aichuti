import os
import io
import zipfile
import shutil
import asyncio
from fastapi import FastAPI, UploadFile, File, Form, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import openai
from openai import AsyncOpenAI
import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import pdfplumber
from PIL import Image
import pytesseract

app = FastAPI()

class TeacherConfig(BaseModel):
    api_url: str
    api_key: str
    model_name: str
    category: str
    prompt_template: str
    use_ocr: bool = False

class VerifyConfig(BaseModel):
    api_url: str
    api_key: str
    model_name: str

class DownloadRequest(BaseModel):
    markdown_text: str
    mode: str

class DeleteRequest(BaseModel):
    category: str

# 👉 新增创建文件夹的数据结构
class CreateFolderRequest(BaseModel):
    category: str

def create_exam_word(markdown_content, mode='student'):
    doc = docx.Document()
    style = doc.styles['Normal']
    style.font.name = '宋体'
    style.font.size = Pt(11)
    
    title = "《建筑材料》考试试卷" if mode == 'student' else "《建筑材料》考试试卷 (教师标准答案版)"
    h = doc.add_heading(title, 0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER

    questions = re.findall(r'\*\*(\d+)\.\s+\[(.*?)\]\*\*(.*?)(<details>.*?</details>)', markdown_content, re.S)
    
    if not questions:
        doc.add_paragraph("⚠️ 提示：试卷解析失败，AI 未完全遵守排版格式，已回退为纯文本模式：\n")
        doc.add_paragraph(markdown_content[:2000])
    else:
        for q_num, q_type, q_body, q_details in questions:
            ans, desc = "", ""
            ans_m = re.search(r'<b>答案：</b>\s*(.*?)\s*<span', q_details)
            if ans_m: ans = ans_m.group(1).strip()
            desc_m = re.search(r'<b>解析：</b>\s*(.*?)\s*</blockquote>', q_details, re.S)
            if desc_m: desc = desc_m.group(1).strip()

            q_body = q_body.strip()
            q_body = re.sub(r'\n正确\s*\n错误\s*$', '', q_body).strip()

            stem, opts = q_body, ""
            opt_match = re.search(r'\nA\..*', q_body, re.S)
            if opt_match:
                stem = q_body[:opt_match.start()].strip()
                opts = opt_match.group(0).strip()

            p = doc.add_paragraph()
            if mode == 'teacher':
                p.add_run(f"{q_num}. [{q_type}] {stem} ( ").bold = True
                ans_run = p.add_run(ans)
                ans_run.font.color.rgb = RGBColor(255, 0, 0)
                ans_run.bold = True
                p.add_run(" )").bold = True
            else:
                p.add_run(f"{q_num}. [{q_type}] {stem} (    )").bold = True

            if opts:
                opt_lines = [o.strip() for o in opts.split('\n') if o.strip()]
                total_len = sum(len(o) for o in opt_lines)
                if total_len < 30: 
                    doc.add_paragraph("\t\t".join(opt_lines))
                elif total_len < 60 and len(opt_lines) >= 4:
                    doc.add_paragraph("\t\t".join(opt_lines[:2]))
                    doc.add_paragraph("\t\t".join(opt_lines[2:]))
                else:
                    for o in opt_lines: doc.add_paragraph(o)

            if mode == 'teacher' and desc:
                desc_p = doc.add_paragraph()
                r = desc_p.add_run(f"【解析】：{desc}")
                r.font.color.rgb = RGBColor(255, 0, 0)
                r.font.size = Pt(10)

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

@app.post("/verify_api/")
def verify_api(config: VerifyConfig):
    client = openai.OpenAI(api_key=config.api_key, base_url=config.api_url, timeout=10.0)
    try:
        client.chat.completions.create(model=config.model_name, messages=[{"role":"user","content":"Hi"}], max_tokens=5)
        return {"status": "success", "message": "连接成功！主线程畅通！"}
    except Exception as e:
        return {"status": "error", "message": f"连接失败: {str(e)}"}

@app.get("/list_folders/")
def list_folders():
    base_path = "/app/uploads/"
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
    folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    if "建筑材料" not in folders:
        folders.insert(0, "建筑材料")
    return {"folders": folders}

# 👉 新增接口：真正让服务器端物理创建分类文件夹
@app.post("/create_folder/")
def create_folder(req: CreateFolderRequest):
    folder_path = f"/app/uploads/{req.category}"
    os.makedirs(folder_path, exist_ok=True)
    return {"message": "物理文件夹创建成功"}

@app.post("/upload_docs/")
async def upload_document(file: UploadFile = File(...), category: str = Form(...)):
    folder_path = f"/app/uploads/{category}"
    os.makedirs(folder_path, exist_ok=True)
    with open(f"{folder_path}/{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"message": "上传成功"}

@app.get("/list_docs/")
def list_documents(category: str):
    folder_path = f"/app/uploads/{category}"
    if not os.path.exists(folder_path): return {"files": []}
    files = [{"name": f} for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return {"files": files}

@app.post("/delete_folder/")
def delete_folder(req: DeleteRequest):
    folder_path = f"/app/uploads/{req.category}"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    return {"message": "分类及其文件已彻底删除"}

@app.post("/generate_exam/")
async def generate_exam(config: TeacherConfig):
    client = AsyncOpenAI(api_key=config.api_key, base_url=config.api_url, timeout=1200.0)
    folder_path = f"/app/uploads/{config.category}"
    
    async def exam_generator():
        docs_text = ""
        yield "> 🚀 **系统启动：准备开始全量阅读资料库...**\n\n"
        
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            for filename in files:
                file_path = os.path.join(folder_path, filename)
                yield f"> 📄 正在解析文件：`{filename}` ...\n\n"
                await asyncio.sleep(0.1) 
                
                if filename.endswith(".docx"):
                    docs_text += f"\n\n【Word资料：{filename}】\n"
                    try:
                        doc = docx.Document(file_path)
                        docs_text += "\n".join([p.text for p in doc.paragraphs])
                        if config.use_ocr:
                            yield f"> 🔍 检测到图文引擎，正在扫描 `{filename}` 中的插图...\n\n"
                            with zipfile.ZipFile(file_path) as docx_zip:
                                for item in docx_zip.namelist():
                                    if item.startswith('word/media/'):
                                        img_data = docx_zip.read(item)
                                        img = Image.open(io.BytesIO(img_data))
                                        ocr_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
                                        if ocr_text.strip(): docs_text += f"\n[图片扫描补充]: {ocr_text.strip()}\n"
                    except Exception as e:
                        pass
                
                elif filename.endswith(".pdf"):
                    docs_text += f"\n\n【PDF资料：{filename}】\n"
                    try:
                        with pdfplumber.open(file_path) as pdf:
                            for page_num, page in enumerate(pdf.pages):
                                text = page.extract_text()
                                if text and len(text.strip()) > 20:
                                    docs_text += text + "\n"
                                elif config.use_ocr:
                                    yield f"> 🔍 对 `{filename}` 第 {page_num + 1} 页进行 OCR...\n\n"
                                    img = page.to_image(resolution=200).original
                                    ocr_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
                                    docs_text += f"\n[PDF扫描件提取]: {ocr_text.strip()}\n"
                    except Exception as e:
                        pass

        if not docs_text.strip():
            yield "❌ **错误：未能在资料库中提取到任何文字。**"
            return
            
        yield f"> ✅ **所有资料均已一字不落阅读完毕！（共提取约 {len(docs_text)} 字符）**\n"
        yield "> 🧠 **资料已输入大模型，正在结合知识点进行全局思考...**\n\n---\n\n"

        try:
            api_task = asyncio.create_task(
                client.chat.completions.create(
                    model=config.model_name,
                    messages=[
                        {"role": "system", "content": config.prompt_template},
                        {"role": "user", "content": f"资料库环境已就绪。以下是系统提取的全量资料：\n{docs_text}\n\n请严格分析上述资料生成考题。"}
                    ],
                    temperature=0.7,
                    stream=True
                )
            )

            while not api_task.done():
                yield "\u200B"
                try:
                    await asyncio.wait_for(asyncio.shield(api_task), timeout=5.0)
                except asyncio.TimeoutError:
                    continue

            response = api_task.result()
            async for chunk in response:
                if hasattr(chunk, 'choices') and chunk.choices and len(chunk.choices) > 0:
                    content = getattr(chunk.choices[0].delta, 'content', None)
                    if content:
                        yield content

        except Exception as e:
            yield f"\n\n"

    return StreamingResponse(exam_generator(), media_type="text/plain")

@app.post("/download_word/")
def download_word(req: DownloadRequest):
    file_stream = create_exam_word(req.markdown_text, req.mode)
    filename = "student_exam.docx" if req.mode == 'student' else "teacher_exam.docx"
    return Response(
        content=file_stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
