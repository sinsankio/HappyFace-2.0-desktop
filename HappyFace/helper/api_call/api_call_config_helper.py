class ApiCallConfigHelper:
    BASE_URL = "http://127.0.0.1:8000/happyface/v2"
    WORK_EMOTION_ENTRY_UPLOAD_ENDPOINT = f"{BASE_URL}/orgs/emotions?org_key=%s"
    WORK_EMOTION_CONSULTANCY_SETUP_ENDPOINT = f"{BASE_URL}/orgs/consultation?org_key=%s"
