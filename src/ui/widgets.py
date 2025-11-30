import streamlit as st

class FileUploadWidget:
    def __init__(self, label, key, type=["jpg", "jpeg", "png"]):
        self.label = label
        self.type = type
        self.key = key
        self.files_ = []   # persistent in this widget instance only

    def render(self):
        uploaded = st.file_uploader(
            self.label,
            type = self.type,
            key = self.key,
            accept_multiple_files=True
        )

        if uploaded:
            for f in uploaded:
                # Avoid duplicates inside this widget
                if f.name not in [fi["name"] for fi in self.files_]:
                    self.files_.append({
                        "name": f.name,
                        "bytes": f.getvalue()
                    })

        return self.files_

    @property
    def files(self):
        return self.files_

    def clear_all(self):
        self.files_ = []
