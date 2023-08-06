from remote_run_everything import Conf, Local, Remote, Down


def test():
    c = Conf(
        host="127.0.0.1",
        user="root",
        pwd='123456',
        remote_root="/mnt/myrust/ssl",
        local_root="D://mygit/remote_run_everything",
    )
    # r = Remote(c)
    l = Local(c)

    # step1:代码文件同步：这个命令会把local_root下的子文件夹递归复制到remote_root对应的子文件夹,虚拟机共享文件夹不需要本步骤
    l.upload(c.local_root, exclude=["node_modules"])

    # step2: 命令行：这个命令会在远程环境remot_root文件夹中执行cargo run，并把输出结果打印在屏幕。多个命令以列表形式传递
    # r.cmd(['cargo run'])

    # step3：代码智能补全文件下载： 这个命令会把remote_root的子文件夹复制到local_root对应子文件夹,虚拟机共享文件夹不需要本步骤，这一步的意义在于ide智能补全（编译代码在虚拟机，本地没有）。实际中，执行此步骤需要根据语言变更子文件夹,以rust为例，复制target即可

    # l.download(c.remote_root+"/target")

    # print (l.upload_scripts())


def test2():
    import requests
    url = ""
    remote_root = "/data/mypy/wmsApi"
    local_root = "D://wmsApi"
    req = requests.post(f"{url}/down/path", json={"root": remote_root})
    files = req.json()
    d = Down()
    print (d.all_path("D://mypy/wq"))

    for remote_path in files:
        # print("begin====", remote_path)
        loc = Down().cli_remote2loc(remote_root, remote_path, local_root)
        url = f"{url}/down/content?path={remote_path}"
        r = requests.get(url, allow_redirects=True)
        d.cli_write(loc, r.content)


test2()
