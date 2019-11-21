much of this is ad-hoc, so there are a couple of manual steps required to reproduce 
the intended result

1. include a .ads\_key file with the text of your api key in the folder above this one

2. the file ascl\_codes must be obtained through a wget or lynx download, with
some manipulation to list every code line by line

this is what I did:
* edit /etc/lynx/lynx.cfg to have persistent cookies
* log in to ascl.net/adm with lynx
* lynx -width=999 -dump -nolist -nomargins http://ascl.net/code/utility/ascl2 |  awk -F: '{if (NF==2) { print "#",$0} else {print $0} }' > ascl2a.txt
* sed -i s/\#//g ascl2a.txt
* awk -F: '{print $2}' ascl2a.txt | awk '{printf("ascl.%s %s\n",$2,$3)}' > ascl2b.txt 
* awk '{print $1}' ascl2b.txt  > ascl\_codes



3. the file ads\_codes is obtained by running ads\_checker.py

4. code\_comparison looks at ads\_codes and checks if each of the lines appears 
in ascl\_codes


