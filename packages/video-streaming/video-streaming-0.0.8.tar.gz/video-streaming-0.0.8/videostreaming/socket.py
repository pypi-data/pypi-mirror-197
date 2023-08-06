import socket, pickle, struct, imutils

class Server():
    def __init__(self, print_ip=True):
        """
        Streaming server socket.\n
        Parameters
        ----------
        - ``print_ip`` : print server IP address (default=True).\n
        Methods
        -------
        - ``connect()`` : open connections for a client socket.
        - ``send()`` : send a frame to the client socket.
        - ``receive()`` : receive a frame from the client socket.
        - ``stop()`` : interrupt all the connections and shut down the server.
        """
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_name  = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        if print_ip:
            print(f"[Server] Host IP: {self.host_ip}")

    def _get_port(self):
        """
        Accepts only 4 numerical digits input!\n
        Returns
        -------
        - ``str`` : user input.
        """
        while True:
            port = input("[Server] >> Select port: ")
            if len(port) == 4:
                try:
                    port = int(port)
                    break
                except:
                    print("[Server] Port not valid!")
            else:
                print("[Server] Port not valid!")
        return port

    def start(self, port=None):
        """
        Wait for a client socket connection.\n
        Parameters
        ----------
        - ``set_port`` (int) : set the port to open for connections (default: False)\n
        Returns
        -------
        - ``True`` : if started correctly.
        - ``False`` : if can"t start.\n
        Example
        -------
        >>> server = Server()
        >>> server.start(port=8888)
        """
        self.__init__(print_ip=False)
        if not port:
            port = self._get_port()
        socket_address = (self.host_ip, port)
        self.server_socket.bind(socket_address)
        self.server_socket.listen(5)
        print(f"[Server] Listening at: {self.host_ip}:{str(port)}")
        try:
            self.client_socket, address = self.server_socket.accept()
            print(f"[Server] Got connection from: {address[0]}")
            return True
        except:
            return False

    def send(self, frame, resolution="high"):
        """
        Send a frame to the client socket.\n
        Parameters
        ----------
        - ``frame`` (cv2 obj) : the frame to send.
        - ``resolution`` (str, int) : the frame resolution.
        can be "high" (1920px), "medium" (1366px), "low" (1024px)
        or an int (default: "high").\n
        Example
        -------
        >>> import cv2
        >>>
        >>> server = Server()
        >>> video = cv2.VideoCapture(0)
        >>>
        >>> while True:
        >>>     if server.start(port=8888)
        >>>         while server.has_client():
        >>>             capturing, frame = video.read()
        >>>             if caputuring:
        >>>                 server.send(frame, "high")
        """
        if resolution == "high":
            resolution = 1920
        elif resolution == "medium":
            resolution = 1366
        elif resolution == "low":
            resolution = 1024
        elif type(resolution) == int:
            pass
        frame = imutils.resize(frame, width=resolution)
        serialized_frame = pickle.dumps(frame)
        message = struct.pack("Q", len(serialized_frame)) + serialized_frame
        try:
            self.client_socket.sendall(message)
        except Exception as error:
            print(error)
            raise Exception(error)

    def receive(self, download_speed=2):
        """
        Receive a frame from the client socket.\n
        Parameters
        ----------
        - ``download_speed`` (float): max download speed (MB) reachable on the network,
        set a value below the effective maximum to avoid errors (default: 2).\n
        Returns
        -------
        - ``True`` , ``frame`` (cv2 obj) : if receiving data.
        - ``False`` , ``None`` : if not receiving data.\n
        Example
        -------
        >>> import cv2
        >>>
        >>> server = Server()
        >>>
        >>> while True:
        >>>     if server.start(port=8888)
        >>>         while server.has_client():
        >>>         receiving, frame = server.receive()
        >>>             if receiving:
        >>>                 cv2.imshow("", frame)
        """
        download_speed = download_speed*1000*1024
        data = b""
        payload_size = struct.calcsize("Q")
        try:
            while len(data) < payload_size:
                packet = self.client_socket.recv(download_speed)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(download_speed)
                if not data:
                    break
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            return True, frame
        except:
            return False, None

    def has_client(self):
        """
        Check if a client is connected with the server.\n
        Returns
        -------
        - ``False`` : if no client connected.
        - ``socket`` (obj) : if client connected.\n
        Example
        -------
        >>> server = Server()
        >>>
        >>> while True:
        >>>     if server.start(port=8888)
        >>>         while client.connected():
        >>>             # do task
        """
        try:
            return self.client_socket
        except:
            return False

    def stop(self):
        """
        Interrupt the connection with the client socket.
        """
        self.server_socket.close()
        print("[Server] Stopped")

class Client():
    def __init__(self):
        """
        Streaming client socket.\n
        Methods
        -------
        - ``connect()`` : connect to the server socket;
        - ``send()`` : send a frame to the server socket;
        - ``receive()`` : receive a frame from the server socket;
        - ``disconnect()`` : disconnect from the server socket.
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _get_ip(self):
        """
        Returns
        -------
        - ``str`` : user input.
        """
        return input("[Client] >> Select ip: ")

    def _get_port(self):
        """
        Accepts only 4 numerical digits input!\n
        Returns
        -------
        - ``str`` : user input.
        """
        while True:
            port = input("[Client] >> Select port: ")
            if len(port) == 4:
                try:
                    port = int(port)
                    break
                except:
                    print("[Client] Port not valid!")
            else:
                print("[Client] Port not valid!")
        return port

    def connect(self, host_ip=None, port=None):
        """
        Connect to the server socket.\n
        Parameters
        ----------
        - ``host_ip`` : set the host ip,
         if None, get input (default=None).
         - ``port`` : set the host port,
         if None, get input (default=None).
        """
        self.__init__()
        if not host_ip:
            host_ip = self._get_ip()
        if not port:
            port = self._get_port()
        try:
            self.client_socket.connect((host_ip, port))
            print(f"[Client] Connected at: {host_ip}")
        except:
            pass


    def send(self, frame, resolution="high"):
        """
        Send a frame to the client socket.\n
        Parameters
        ----------
        - ``frame`` (cv2 obj) : the frame to send.
        - ``resolution`` (str, int) : the frame resolution.
        can be "high" (1920px), "medium" (1366px), "low" (1024px)
        or an int (default: "high").\n
        Example
        -------
        >>> import cv2
        >>>
        >>> client = Client()
        >>> video = cv2.VideoCapture(0)
        >>>
        >>> while True:
        >>>     client.connect(port=8888)
        >>>     while client.is_connected():
        >>>         capturing, frame = video.read()
        >>>         if caputuring:
        >>>             client.send(frame, "high")
        """
        if resolution == "high":
            resolution = 1920
        elif resolution == "medium":
            resolution = 1366
        elif resolution == "low":
            resolution = 1024
        elif type(resolution) == int:
            pass
        frame = imutils.resize(frame, width=resolution)
        serialized_frame = pickle.dumps(frame)
        message = struct.pack("Q", len(serialized_frame)) + serialized_frame
        try:
            self.client_socket.sendall(message)
        except Exception as error:
            print(error)
            raise Exception(error)

    def receive(self, download_speed=2):
        """
        Receive a frame from the server socket.\n
        Parameters
        ----------
        - ``download_speed`` (float): max download speed (MB) reachable on the network,
        set a value below the effective maximum to avoid errors (default: 2).\n
        Returns
        -------
        - ``True`` , ``frame`` (cv2 obj) : if receiving data.
        - ``False`` , ``None`` : if not receiving data.\n
        Example
        -------
        >>> import cv2
        >>>
        >>> client = Client()
        >>>
        >>> while True:
        >>>     client.connect(host_ip="127.0.0.1", port=8888)
        >>>     while client.is_connected():
        >>>         receiving, frame = client.receive()
        >>>             if receiving:
        >>>                 cv2.imshow("", frame)
        """
        download_speed = download_speed*1000*1024
        data = b""
        payload_size = struct.calcsize("Q")
        try:
            while len(data) < payload_size:
                packet = self.client_socket.recv(download_speed)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(download_speed)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            return True, frame
        except:
            return False, None

    def is_connected(self):
        return True

    def disconnect(self):
        """
        Interrupt the connection with the client socket.
        """
        self.client_socket.close()
        print("[Client] Disconnected")