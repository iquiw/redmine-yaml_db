from io import BytesIO
import os
import tarfile

def docker_copyto(container, srcfile, dstdir):
    tarstream = BytesIO()
    tar = tarfile.open(fileobj = tarstream, mode = 'w')
    tar.add(srcfile)
    tar.close()
    tarstream.seek(os.SEEK_SET)

    return container.put_archive(data = tarstream, path = dstdir)
