from io import BytesIO
import os
from pathlib import PurePosixPath
import tarfile

def docker_copyto(container, srcfile, dstfile):
    p = PurePosixPath(dstfile)
    dstdir = p.parent
    dstname = p.name
    tarstream = BytesIO()
    tar = tarfile.open(fileobj = tarstream, mode = 'w')
    tar.add(srcfile, arcname = dstname)
    tar.close()
    tarstream.seek(os.SEEK_SET)

    return container.put_archive(data = tarstream, path = dstdir)
