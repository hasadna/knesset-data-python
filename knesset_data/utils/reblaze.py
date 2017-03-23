def is_reblaze_content(content, raise_exception=False):
    if '<html><head><meta charset="utf-8"></head><body><script>window.rbzns' in content:
        if raise_exception:
            raise Exception("seems you are blocked by Knesset reblaze, sorry")
        else:
            return True
    else:
        return False
