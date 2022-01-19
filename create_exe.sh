pyinstaller --onefile \
            --hidden-import=time \
            --hidden-import=datetime \
            --hidden-import=smtplib \
            --hidden-import=json \
            --hidden-import=os \
            --hidden-import=sys \
            --hidden-import=email.mime \
            --hidden-import=email.encoders \
            --hidden-import=zipfile \
            --distpath ./result \
            --windowed result.py
# --hidden-import=