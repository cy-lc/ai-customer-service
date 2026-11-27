import hashlib
class HashCalculate:
    def compute_hash(self,pdf_bytes:bytes):
        return hashlib.md5(pdf_bytes).hexdigest()


    def compute_hash_from_file(self,file_path:str):
        hash_md5=hashlib.md5()
        with open(file_path,'rb') as f:
            for chunk in iter(lambda: f.read(4096),b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
 
if __name__=='__main__':

    hash_calculate=HashCalculate()
    path="C:\\Users\\30133\\PycharmProjects\\WelcomeScreen\\study\\smart_reading\\3038344414dcf5ef18132fe3fe396e55.pdf"
    print(hash_calculate.compute_hash_from_file(path))


