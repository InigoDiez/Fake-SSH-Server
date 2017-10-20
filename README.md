# Fake-SSH-Server
En este proyecto se ha desarrollado un script en lenguaje python, cuyo objetivo es simular un servidor SSH falso el cual solo permite autorización mediante usuario y contraseña. 
El servidor almacena las credenciales con las que intentan conectarse a el y prueba en el otro extremo de la conexión las mismas credenciales. Es decir, lo que hace es probar las credenciales con las que intenta entrar el cliente en el mismo cliente, y en caso de tener el cliente un usuario y contraseña igual a los que ha probado el servidor almacena la ip y las credenciales en un archivo de nombre "Credenciales.txt".
Adicionalmente dicho servidor siempre devuelve credenciales incorrectas manteniendo de esta manera la máquina segura.
Es necesario ejecutar el programa con privilegios de root ya que el puerto que utiliza es el de SSH, 22.
