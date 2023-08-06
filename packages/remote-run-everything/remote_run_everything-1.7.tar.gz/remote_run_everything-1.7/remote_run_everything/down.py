import glob, pathlib, os, requests


class Down:
    '''用于内网环境部署,服务端需要给出所有路径(使用all path),客户端拉代码
    服务端例子 fastapi

@toolView.post("/down/path")
async def all_file(request: Request):
    arg = await request.json()
    root = arg.get("root", "")
    print("root===", root)
    if root != "":
        res = Down().all_path(root)
        return res


@toolView.get("/down/content")
async def download(request: Request, path: str):
    return FileResponse(path=path, filename=os.path.basename(path))


    '''

    def __init__(self):
        self.drop_extention = ['.pyc', '.pickle', ".tar", ".log", ".rar", ".zip"]

    def all_path(self, root):
        '''服务端提供的接口
        '''
        if not os.path.exists(root):
            return []
        files = glob.glob(f'{root}/**/*', recursive=True)
        res = []
        for path in files:
            if os.path.isdir(path):
                continue
            file_extension = pathlib.Path(path).suffix
            if file_extension not in self.drop_extention:
                res.append(path)
        return res

    def cli_remote2loc(self, remote_root, remote_path, local_root):
        relpath = os.path.relpath(remote_path, start=remote_root)
        loc = os.path.join(local_root, relpath)
        return loc

    def cli_write(self, loc, content):
        dir = os.path.dirname(loc)
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
        with open(loc, "wb") as f:
            f.write(content)
            os.chmod(loc, 0o777)
