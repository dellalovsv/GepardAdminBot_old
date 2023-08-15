def check_cancel(cancel: str) -> bool:
    if cancel.strip() == '/cancel' or cancel.strip() == 'cancel':
        return True
    else:
        return False
