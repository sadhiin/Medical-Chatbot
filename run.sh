# python -m venv venv
# source venv/bin/activate
pip install update pip
pip install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/
pip install -r requirements.txt

# python main.py
uvicorn main:app --reload