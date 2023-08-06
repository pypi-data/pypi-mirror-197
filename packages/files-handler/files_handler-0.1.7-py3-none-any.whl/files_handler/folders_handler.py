import os
import shutil
class folders_handler:

    def __init__(self, path_ref):
        self.path_ref = path_ref

    def clear_folder(self, folder_path_to_clear):
        """
        Clear the folder, or file
        
        :param folder_path_to_clear: the path of the folder to clear 
        :type folder_path_to_clear: string
    
        :return: void
        """
        path_to_clear = os.path.join(self.path_ref, folder_path_to_clear)
        print(f"Clearing: {path_to_clear}")

        if os.path.exists(path_to_clear) and os.path.isdir(path_to_clear):
            shutil.rmtree(path_to_clear)
        elif os.path.exists(path_to_clear) and os.path.isfile(path_to_clear):
            os.remove(path_to_clear)

    def verify_and_create_folder(self, folder_path_to_create, message=''):
        """
        Verify and Create a Folder
        
        :param folder_path_to_create: the path of the folder to create 
        :type folder_path_to_create: string
    
        :return: if the folder not exists create the folder and returns True, if exists returns False
        :type: boolean 
        """
        path_to_create = os.path.join(self.path_ref, folder_path_to_create)
        print(f"Verifying and creating folder: {path_to_create}")
        if not os.path.exists(path_to_create):
            print(message)
            os.makedirs(path_to_create)
            return True
        return False