Docker scripts for Linux shell *.sh and Windows Power Shell *.cmd

-> Place this folder in the home directory of the current user ( /home/<user> or C:\Users\<user> ) (and do not rename it).

-> Place the SESToPy files ... main.py etc. ... in this folder.

-> "Docker_0_Build_Image" builds an image with the help of the dockerfile, which loads an existing Ubuntu 18.04 image, installs Python3, PyQt5 and nano, and copies the SESToPy files into the /app directory of the image.
                          SESToPy ist started. Remember that the IP 127.0.0.1 is the localhost of the docker container. When connecting to SESViewEl the IP of the SESViewEl host needs to be entered.  

-> "Docker_1_Start_Container" starts a container from this image.

-> "Docker_2_Show_All_Infos": Shows all infos of images, started containers, ports, etc.

-> "Docker_3_Enter_Container_Shell": Executing in a shell, it gives access to a shell in the container.

-> "Docker_4_Stop_Remove_Container" stops and deletes the container.

-> "Docker_5_Save_Image" saves the image in the home directory of the current user.

-> "Docker_6_Delete_Image" deletes the image.

-> "Docker_7_Load_Image" loads the saved image back.

-> "Docker_8_Remove_all_Containers_and_Images" removes all containers and images from an docker registry on the computer.

Linux shellscripts:

-> If the shellscript(s) cannot be executed, make sure they are marked as executable. Furthermore they need to be owned by the current user and be in the group of the current user.

-> Error: /bin/sh^M: Broken interpreter: File or directory not found
   The ^M is a carriage return character. Linux uses the line feed character to mark the end of a line, whereas Windows uses the two-character sequence CR LF. Your file has Windows line endings, which is confusing Linux. Correct with the command:
   sed -i -e 's/\r$//' scriptname.sh
