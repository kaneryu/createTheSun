if __name__ == '__main__':
    print("This is a module, Not a program.")
else:
    import base64
    def base64Encode(s):
        return base64.b64encode(s.encode()).decode()
    def base64Decode(s):
        return base64.b64decode(s).decode()

    