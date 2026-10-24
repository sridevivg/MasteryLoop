"""
Computer Networks Question Bank.
Topic 1: Protocol Architectures (15 questions across NET_OSI_MODEL, NET_APPLICATION)
Topic 2: Transport & Routing (15 questions across NET_TCP_UDP, NET_IP_ROUTING)
"""

NETWORKS_ITEMS = [
    # =========================================================================
    # TOPIC 1: Protocol Architectures (15 items)
    # =========================================================================
    # --- NET_OSI_MODEL (8 items) ---
    {
        "skill_code": "NET_OSI_MODEL",
        "stem": "Which layer of the OSI 7-layer reference model is responsible for end-to-end process-to-process communication, flow control, and segmentation?",
        "options": [
            {"id": "A", "text": "Transport Layer (Layer 4)", "is_distractor": False},
            {"id": "B", "text": "Network Layer (Layer 3)", "is_distractor": True},
            {"id": "C", "text": "Data Link Layer (Layer 2)", "is_distractor": True},
            {"id": "D", "text": "Session Layer (Layer 5)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The Transport Layer (Layer 4, protocols TCP/UDP) handles port-to-port multiplexing, flow control, reliability, and segmentation of application payloads.",
        "distractor_explanations": {
            "B": "Network Layer (IP) handles host-to-host routing and logical addressing.",
            "C": "Data Link Layer handles node-to-node framing and MAC addressing.",
            "D": "Session Layer establishes, manages, and terminates dialog sessions."
        },
        "a": 1.25,
        "b": -1.10,
        "point_biserial": 0.40
    },
    {
        "skill_code": "NET_OSI_MODEL",
        "stem": "What is the Protocol Data Unit (PDU) name at the Data Link Layer (Layer 2)?",
        "options": [
            {"id": "A", "text": "Frame", "is_distractor": False},
            {"id": "B", "text": "Packet", "is_distractor": True},
            {"id": "C", "text": "Segment", "is_distractor": True},
            {"id": "D", "text": "Bit stream", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "PDUs by layer: Physical = Bits, Data Link = Frames, Network = Packets, Transport = Segments (TCP) / Datagrams (UDP), Application = Message/Data.",
        "distractor_explanations": {
            "B": "Packet is the Layer 3 (Network) PDU.",
            "C": "Segment is the Layer 4 (Transport) PDU.",
            "D": "Bits is the Layer 1 (Physical) PDU."
        },
        "a": 1.30,
        "b": -0.80,
        "point_biserial": 0.41
    },
    {
        "skill_code": "NET_OSI_MODEL",
        "stem": "At which layer of the OSI model does a traditional standard Ethernet Switch operate?",
        "options": [
            {"id": "A", "text": "Data Link Layer (Layer 2)", "is_distractor": False},
            {"id": "B", "text": "Network Layer (Layer 3)", "is_distractor": True},
            {"id": "C", "text": "Physical Layer (Layer 1)", "is_distractor": True},
            {"id": "D", "text": "Application Layer (Layer 7)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Standard network switches inspect Layer 2 Ethernet frame headers to learn source MAC addresses and forward frames using a MAC address table (CAM table).",
        "distractor_explanations": {
            "B": "Routers (and multilayer switches) operate at Layer 3 using IP addresses.",
            "C": "Hubs and repeaters operate at Layer 1.",
            "D": "Application gateways and reverse proxies operate at Layer 7."
        },
        "a": 1.35,
        "b": -0.40,
        "point_biserial": 0.42
    },
    {
        "skill_code": "NET_OSI_MODEL",
        "stem": "What function does the **Presentation Layer (Layer 6)** perform in the OSI model?",
        "options": [
            {"id": "A", "text": "Data format translation, encryption/decryption (e.g. TLS), and compression", "is_distractor": False},
            {"id": "B", "text": "Hardware electrical signaling across copper twisted pair", "is_distractor": True},
            {"id": "C", "text": "Subnet routing across autonomous systems", "is_distractor": True},
            {"id": "D", "text": "Media Access Control (MAC) collision resolution", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Layer 6 ensures data sent from the application layer of one system can be read by the application layer of another, handling ASCII/EBCDIC conversion, compression, and cryptography.",
        "distractor_explanations": {
            "B": "Physical Layer function.",
            "C": "Network Layer routing function (BGP/OSPF).",
            "D": "Data Link Layer CSMA/CD function."
        },
        "a": 1.45,
        "b": 0.15,
        "point_biserial": 0.44
    },
    {
        "skill_code": "NET_OSI_MODEL",
        "stem": "What is the primary role of the **Address Resolution Protocol (ARP)** in networking?",
        "options": [
            {"id": "A", "text": "Translating an IPv4 network layer address into a physical Data Link Layer MAC address on the local network segment.", "is_distractor": False},
            {"id": "B", "text": "Translating domain names into IP addresses.", "is_distractor": True},
            {"id": "C", "text": "Assigning dynamic IP configurations to client machines.", "is_distractor": True},
            {"id": "D", "text": "Encrypting payload data between client and server.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "ARP broadcasts on the local Layer 2 broadcast domain (`FF:FF:FF:FF:FF:FF`) asking 'Who has IP X.X.X.X? Tell MAC Y.Y.Y.Y', mapping Layer 3 IP to Layer 2 MAC.",
        "distractor_explanations": {
            "B": "Describes Domain Name System (DNS).",
            "C": "Describes Dynamic Host Configuration Protocol (DHCP).",
            "D": "Describes TLS/SSL or IPsec."
        },
        "a": 1.40,
        "b": -0.20,
        "point_biserial": 0.43
    },
    {
        "skill_code": "NET_OSI_MODEL",
        "stem": "In the TCP/IP 5-layer practical model, how are the top three OSI layers (Session, Presentation, Application) handled?",
        "options": [
            {"id": "A", "text": "They are consolidated into a single unified Application Layer.", "is_distractor": False},
            {"id": "B", "text": "They are omitted completely as unnecessary.", "is_distractor": True},
            {"id": "C", "text": "They are implemented inside the OS network driver at Layer 2.", "is_distractor": True},
            {"id": "D", "text": "They are embedded into the IP header.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The Internet Architecture (TCP/IP) collapses Session, Presentation, and Application into a single Application Layer, delegating session management and encryption directly to application protocols (HTTP, SSH, TLS).",
        "distractor_explanations": {
            "B": "The functionalities are preserved, but located within application software.",
            "C": "Network drivers operate at Layer 2 (Data Link).",
            "D": "IP headers operate strictly at Layer 3."
        },
        "a": 1.50,
        "b": 0.40,
        "point_biserial": 0.45
    },
    {
        "skill_code": "NET_OSI_MODEL",
        "stem": "What is **Encapsulation** as a packet travels down the network protocol stack from sender to wire?",
        "options": [
            {"id": "A", "text": "Each descending layer wraps the higher-layer payload with its own protocol header (and optional trailer) containing metadata.", "is_distractor": False},
            {"id": "B", "text": "Data compression that reduces overall payload byte size.", "is_distractor": True},
            {"id": "C", "text": "Converting analog signals to digital pulses.", "is_distractor": True},
            {"id": "D", "text": "Stripping headers to expose the raw data bytes.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "As data descends the stack, the Transport layer adds a TCP/UDP header (Segment), the Network layer adds an IP header (Packet), and the Data Link layer adds a frame header and FCS trailer (Frame).",
        "distractor_explanations": {
            "B": "Compression is distinct from protocol encapsulation.",
            "C": "Modulation/encoding handles signal conversion at Layer 1.",
            "D": "Stripping headers is Decapsulation on the receiving end."
        },
        "a": 1.35,
        "b": -0.65,
        "point_biserial": 0.42
    },
    {
        "skill_code": "NET_OSI_MODEL",
        "stem": "What is the function of the **Maximum Transmission Unit (MTU)** at the Data Link layer (typically 1500 bytes for standard Ethernet)?",
        "options": [
            {"id": "A", "text": "The maximum size of the Layer 3 packet (including IP header and payload) that can be forwarded without fragmentation.", "is_distractor": False},
            {"id": "B", "text": "The total bandwidth limit of the cable in Megabits per second.", "is_distractor": True},
            {"id": "C", "text": "The maximum length of the physical copper cable in meters.", "is_distractor": True},
            {"id": "D", "text": "The maximum number of simultaneous TCP socket connections.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "MTU defines the maximum single IP packet size that can pass over a physical media frame without triggering IP packet fragmentation.",
        "distractor_explanations": {
            "B": "Bandwidth limit is link capacity / line rate.",
            "C": "Maximum cable distance (e.g. 100m for Cat6) is physical attenuation limit.",
            "D": "Socket limits are determined by file descriptor limits and RAM."
        },
        "a": 1.60,
        "b": 0.90,
        "point_biserial": 0.48
    },

    # --- NET_APPLICATION (7 items) ---
    {
        "skill_code": "NET_APPLICATION",
        "stem": "What is the primary architectural difference between **HTTP/1.1** and **HTTP/2**?",
        "options": [
            {"id": "A", "text": "HTTP/2 introduces binary framing and multiplexing of concurrent streams over a single TCP connection, eliminating head-of-line blocking at the application layer.", "is_distractor": False},
            {"id": "B", "text": "HTTP/2 replaces TCP with UDP entirely.", "is_distractor": True},
            {"id": "C", "text": "HTTP/2 eliminates headers.", "is_distractor": True},
            {"id": "D", "text": "HTTP/2 requires plain text without TLS encryption.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "HTTP/1.1 suffered from application-level head-of-line blocking (one request per connection at a time). HTTP/2 uses binary framing to interleave multiple bidirectional streams over a single shared TCP socket.",
        "distractor_explanations": {
            "B": "HTTP/3 replaces TCP with QUIC/UDP, whereas HTTP/2 runs over TCP.",
            "C": "HTTP/2 compresses headers using HPACK, but does not eliminate them.",
            "D": "In modern browsers, HTTP/2 universally requires TLS encryption (h2)."
        },
        "a": 1.50,
        "b": 0.35,
        "point_biserial": 0.46
    },
    {
        "skill_code": "NET_APPLICATION",
        "stem": "In DNS resolution, what is the role of an **Authoritative Name Server**?",
        "options": [
            {"id": "A", "text": "It holds the official, definitive DNS records (e.g., A, AAAA, CNAME, MX) configured by the domain owner for a specific zone.", "is_distractor": False},
            {"id": "B", "text": "It caches queries for ISP residential customers to speed up web browsing.", "is_distractor": True},
            {"id": "C", "text": "It manages the 13 root server clusters globally.", "is_distractor": True},
            {"id": "D", "text": "It acts as a local browser cookie cache.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "An authoritative name server has definitive administrative authority over a DNS zone. Unlike recursive resolvers that merely cache, authoritative servers store master zone files.",
        "distractor_explanations": {
            "B": "Describes a Recursive DNS Resolver (like 8.8.8.8 or ISP DNS).",
            "C": "Describes DNS Root Name Servers.",
            "D": "Browser caches are application software components."
        },
        "a": 1.45,
        "b": -0.15,
        "point_biserial": 0.44
    },
    {
        "skill_code": "NET_APPLICATION",
        "stem": "Which HTTP request method is defined by RFC 9110 as being both **Safe** and **Idempotent**?",
        "options": [
            {"id": "A", "text": "GET", "is_distractor": False},
            {"id": "B", "text": "POST", "is_distractor": True},
            {"id": "C", "text": "DELETE", "is_distractor": True},
            {"id": "D", "text": "PATCH", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A Safe method produces no server side-effects (read-only). An Idempotent method produces identical server state whether executed once or $N$ times. `GET` is both Safe and Idempotent. `DELETE` is Idempotent but not Safe. `POST` is neither.",
        "distractor_explanations": {
            "B": "POST is neither safe nor idempotent (repeated POST creates multiple resources).",
            "C": "DELETE is idempotent, but not safe because it mutates server state by removing items.",
            "D": "PATCH is neither safe nor guaranteed idempotent."
        },
        "a": 1.40,
        "b": -0.35,
        "point_biserial": 0.43
    },
    {
        "skill_code": "NET_APPLICATION",
        "stem": "What is the purpose of the **TLS Handshake** in HTTPS?",
        "options": [
            {"id": "A", "text": "Authenticating the server's identity via X.509 certificate and negotiating a shared symmetric session key (e.g. AES-GCM) via Diffie-Hellman.", "is_distractor": False},
            {"id": "B", "text": "Compressing HTML text files before sending.", "is_distractor": True},
            {"id": "C", "text": "Routing packets across intermediate BGP Autonomous Systems.", "is_distractor": True},
            {"id": "D", "text": "Allocating physical port numbers on client operating systems.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "TLS handshake uses asymmetric cryptography and PKI certificates to verify server authenticity, then establishes a high-throughput symmetric session key for bulk data encryption.",
        "distractor_explanations": {
            "B": "Gzip/Brotli compression is handled at the HTTP protocol layer.",
            "C": "BGP handles Layer 3 inter-domain routing.",
            "D": "Operating system TCP stack assigns ephemeral client ports."
        },
        "a": 1.55,
        "b": 0.65,
        "point_biserial": 0.47
    },
    {
        "skill_code": "NET_APPLICATION",
        "stem": "What happens during a **DNS CNAME record** lookup?",
        "options": [
            {"id": "A", "text": "The queried alias domain is mapped to another canonical domain name, requiring the resolver to look up that new domain's A/AAAA record.", "is_distractor": False},
            {"id": "B", "text": "It returns the IPv4 address immediately in a single step.", "is_distractor": True},
            {"id": "C", "text": "It routes mail traffic to an SMTP relay host.", "is_distractor": True},
            {"id": "D", "text": "It delegates authority to a child nameserver.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A CNAME (Canonical Name) record is an alias pointer. When resolved, the nameserver restarts resolution using the canonical name target.",
        "distractor_explanations": {
            "B": "A records map directly to IPv4 addresses, not CNAME.",
            "C": "MX (Mail Exchange) records route email traffic.",
            "D": "NS (Name Server) records delegate zone authority."
        },
        "a": 1.45,
        "b": 0.05,
        "point_biserial": 0.44
    },
    {
        "skill_code": "NET_APPLICATION",
        "stem": "Which underlying transport protocol is used by **HTTP/3**?",
        "options": [
            {"id": "A", "text": "QUIC (built on top of UDP)", "is_distractor": False},
            {"id": "B", "text": "Standard TCP with TLS 1.3", "is_distractor": True},
            {"id": "C", "text": "SCTP", "is_distractor": True},
            {"id": "D", "text": "Raw IP without transport headers", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "HTTP/3 replaces TCP with Google's QUIC protocol over UDP, eliminating transport-level head-of-line blocking and reducing connection establishment to 0-RTT/1-RTT.",
        "distractor_explanations": {
            "B": "HTTP/2 and HTTP/1.1 run over TCP.",
            "C": "SCTP is a telecom transport protocol, not used in HTTP/3.",
            "D": "Layer 4 transport multiplexing and encryption are mandatory."
        },
        "a": 1.60,
        "b": 0.95,
        "point_biserial": 0.49
    },
    {
        "skill_code": "NET_APPLICATION",
        "stem": "In WebSockets, how does the initial connection establishment occur?",
        "options": [
            {"id": "A", "text": "Via an HTTP/1.1 Upgrade handshake (`Connection: Upgrade`, `Upgrade: websocket`), switching the underlying TCP socket to full-duplex framing.", "is_distractor": False},
            {"id": "B", "text": "By opening a raw UDP port directly from JavaScript in the browser.", "is_distractor": True},
            {"id": "C", "text": "Through recurring HTTP polling every 100 milliseconds.", "is_distractor": True},
            {"id": "D", "text": "By modifying DNS records dynamically.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "WebSocket begins with standard HTTP GET including `Upgrade: websocket`. If the server responds with `101 Switching Protocols`, the TCP connection remains open for bidirectional framing.",
        "distractor_explanations": {
            "B": "Web browsers do not allow arbitrary raw UDP socket access from JavaScript.",
            "C": "Describes long-polling or polling, the exact overhead WebSocket eliminates.",
            "D": "DNS is not modified during socket handshakes."
        },
        "a": 1.50,
        "b": 0.45,
        "point_biserial": 0.46
    },

    # =========================================================================
    # TOPIC 2: Transport & Routing (15 items)
    # =========================================================================
    # --- NET_TCP_UDP (8 items) ---
    {
        "skill_code": "NET_TCP_UDP",
        "stem": "Which sequence correctly represents the flags exchanged during the standard **TCP 3-Way Handshake** to establish a connection?",
        "options": [
            {"id": "A", "text": "SYN -> SYN-ACK -> ACK", "is_distractor": False},
            {"id": "B", "text": "ACK -> SYN -> SYN-ACK", "is_distractor": True},
            {"id": "C", "text": "SYN -> ACK -> FIN", "is_distractor": True},
            {"id": "D", "text": "HELLO -> READY -> ACK", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Client sends SYN (with initial sequence number ISN_c). Server replies with SYN-ACK (ISN_s and ACK = ISN_c + 1). Client acknowledges with ACK (ACK = ISN_s + 1).",
        "distractor_explanations": {
            "B": "Connection initiation must begin with SYN flag, not ACK.",
            "C": "FIN is used to terminate connections, not establish them.",
            "D": "HELLO is not a standard TCP flag."
        },
        "a": 1.25,
        "b": -0.60,
        "point_biserial": 0.40
    },
    {
        "skill_code": "NET_TCP_UDP",
        "stem": "Why does a TCP connection enter the **TIME_WAIT** state on the endpoint that actively closed the connection?",
        "options": [
            {"id": "A", "text": "To ensure the final ACK was received by the peer (retransmitting if lost) and to prevent lingering delayed duplicate packets from corrupting future connections.", "is_distractor": False},
            {"id": "B", "text": "To download remaining buffer files from the hard drive.", "is_distractor": True},
            {"id": "C", "text": "Because the operating system forgot the socket port number.", "is_distractor": True},
            {"id": "D", "text": "To re-establish the connection automatically.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "TIME_WAIT lasts $2 \\times \\text{MSL}$ (Maximum Segment Lifetime, typically 1-2 minutes). It ensures the peer received the final ACK and purges phantom packets from the internet before recycling the tuple (IP, Port).",
        "distractor_explanations": {
            "B": "Data buffers are flushed prior to closing.",
            "C": "The socket state is explicitly maintained in the kernel table.",
            "D": "The connection is being finalized, not re-established."
        },
        "a": 1.55,
        "b": 0.50,
        "point_biserial": 0.47
    },
    {
        "skill_code": "NET_TCP_UDP",
        "stem": "What is the primary difference between **Flow Control** and **Congestion Control** in TCP?",
        "options": [
            {"id": "A", "text": "Flow control protects the receiving endpoint's buffer from overflowing; Congestion control protects the intermediate network routers from buffer saturation.", "is_distractor": False},
            {"id": "B", "text": "Flow control uses UDP, while congestion control uses TCP.", "is_distractor": True},
            {"id": "C", "text": "Flow control is handled by DNS servers; congestion control is handled by BGP.", "is_distractor": True},
            {"id": "D", "text": "They are synonymous terms for sliding window sizing.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Flow control uses the Receiver Window (`rwnd`) communicated in TCP headers. Congestion control uses the Congestion Window (`cwnd`) inferred through latency and packet drop algorithms (AIMD, BBR). Effective window is $\\min(rwnd, cwnd)$.",
        "distractor_explanations": {
            "B": "Both are fundamental subsystems of TCP.",
            "C": "Both are executed by client and server operating system TCP stacks, not DNS/BGP.",
            "D": "They target completely distinct bottlenecks (endpoint receiver memory vs network switches)."
        },
        "a": 1.50,
        "b": 0.20,
        "point_biserial": 0.45
    },
    {
        "skill_code": "NET_TCP_UDP",
        "stem": "In TCP Congestion Control, what happens when **3 duplicate ACKs** are received by the sender under the Fast Retransmit algorithm?",
        "options": [
            {"id": "A", "text": "The sender immediately retransmits the missing segment without waiting for the retransmission timeout (RTO) timer to expire.", "is_distractor": False},
            {"id": "B", "text": "The sender terminates the TCP connection with an RST flag.", "is_distractor": True},
            {"id": "C", "text": "The sender doubles the congestion window size.", "is_distractor": True},
            {"id": "D", "text": "The sender resets the sequence number to 0.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "3 duplicate ACKs signify that subsequent packets arrived at the receiver, but one isolated packet in between was lost. Fast Retransmit infers packet loss immediately, avoiding the heavy idle penalty of a full RTO timer expiration.",
        "distractor_explanations": {
            "B": "RST terminates connections abnormally, which is not desired on mild packet drop.",
            "C": "Congestion window is halved (in Reno/NewReno), not doubled.",
            "D": "Sequence numbers continue monotonically."
        },
        "a": 1.60,
        "b": 0.75,
        "point_biserial": 0.48
    },
    {
        "skill_code": "NET_TCP_UDP",
        "stem": "Why is **UDP** preferred over TCP for real-time video conferencing (e.g. WebRTC) and multiplayer gaming?",
        "options": [
            {"id": "A", "text": "UDP has zero connection overhead, no retransmissions, and no head-of-line blocking, prioritizing low latency over perfect reliability.", "is_distractor": False},
            {"id": "B", "text": "UDP guarantees higher encryption strength.", "is_distractor": True},
            {"id": "C", "text": "UDP automatically scales server bandwidth.", "is_distractor": True},
            {"id": "D", "text": "UDP packets are always delivered in strictly sorted order.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In live audio/video, a delayed late frame is useless. TCP's retransmission mechanism would stall live playback (head-of-line blocking). UDP allows dropping lost frames and playing the newest data immediately.",
        "distractor_explanations": {
            "B": "Encryption is orthogonal to transport layer choice.",
            "C": "Bandwidth is determined by network hardware and transmission rates.",
            "D": "UDP offers no ordering guarantees; packets can arrive out of order."
        },
        "a": 1.35,
        "b": -0.85,
        "point_biserial": 0.41
    },
    {
        "skill_code": "NET_TCP_UDP",
        "stem": "What is the size of the standard **UDP header** compared to the minimum **TCP header**?",
        "options": [
            {"id": "A", "text": "UDP header is 8 bytes; minimum TCP header is 20 bytes.", "is_distractor": False},
            {"id": "B", "text": "UDP header is 20 bytes; minimum TCP header is 8 bytes.", "is_distractor": True},
            {"id": "C", "text": "Both headers are exactly 16 bytes.", "is_distractor": True},
            {"id": "D", "text": "UDP has zero header bytes.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A UDP header contains only 4 fields of 2 bytes each (Source Port, Destination Port, Length, Checksum) = 8 bytes. A base TCP header contains sequence numbers, ack numbers, flags, window sizes = 20 bytes.",
        "distractor_explanations": {
            "B": "Inverted sizes.",
            "C": "Neither is 16 bytes.",
            "D": "UDP requires port multiplexing and length fields (8 bytes total)."
        },
        "a": 1.45,
        "b": 0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "NET_TCP_UDP",
        "stem": "What is the **SYN Flood** Denial of Service attack mechanism?",
        "options": [
            {"id": "A", "text": "An attacker floods a server with TCP SYN packets with spoofed source IPs and never completes the 3-way handshake, exhausting the server's SYN backlog queue.", "is_distractor": False},
            {"id": "B", "text": "An attacker sends invalid UDP packets to crash the router.", "is_distractor": True},
            {"id": "C", "text": "An attacker floods DNS servers with zone transfer queries.", "is_distractor": True},
            {"id": "D", "text": "An attacker repeatedly downloads large video files.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The server allocates half-open TCB state for each incoming SYN and waits for final ACK. By spoofing source IPs, the server's connection table saturates, rejecting legitimate users (mitigated by SYN Cookies).",
        "distractor_explanations": {
            "B": "Describes a UDP flood.",
            "C": "Describes a DNS amplification or AXFR attack.",
            "D": "Describes application layer bandwidth exhaustion."
        },
        "a": 1.55,
        "b": 0.60,
        "point_biserial": 0.46
    },
    {
        "skill_code": "NET_TCP_UDP",
        "stem": "In TCP, what mechanism avoids the **Silly Window Syndrome** on the sender side?",
        "options": [
            {"id": "A", "text": "Nagle's Algorithm", "is_distractor": False},
            {"id": "B", "text": "Clark's Solution", "is_distractor": True},
            {"id": "C", "text": "Dijkstra's Algorithm", "is_distractor": True},
            {"id": "D", "text": "Kahn's Algorithm", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Nagle's Algorithm coalesces small outgoing packets by withholding transmission until a full MSS (Maximum Segment Size) packet accumulates or until the previous ACK is received. Clark's solution operates on the receiver side.",
        "distractor_explanations": {
            "B": "Clark's solution operates on the RECEIVER side (withholding window updates).",
            "C": "Dijkstra is for shortest path graph routing.",
            "D": "Kahn is for topological sorting."
        },
        "a": 1.65,
        "b": 1.30,
        "point_biserial": 0.50
    },

    # --- NET_IP_ROUTING (7 items) ---
    {
        "skill_code": "NET_IP_ROUTING",
        "stem": "In IPv4 subnetting, how many usable host IP addresses are available in a `/26` subnet prefix?",
        "options": [
            {"id": "A", "text": "62 usable hosts", "is_distractor": False},
            {"id": "B", "text": "64 usable hosts", "is_distractor": True},
            {"id": "C", "text": "126 usable hosts", "is_distractor": True},
            {"id": "D", "text": "30 usable hosts", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A `/26` subnet has $32 - 26 = 6$ host bits. Total IP addresses = $2^6 = 64$. We must subtract 2 addresses: the Network ID (all zeros) and the Broadcast address (all ones). Usable hosts = $64 - 2 = 62$.",
        "distractor_explanations": {
            "B": "Forgot to subtract the 2 reserved addresses (Network ID and Broadcast).",
            "C": "126 is the usable host count for a `/25` subnet ($2^7 - 2$).",
            "D": "30 is the usable host count for a `/27` subnet ($2^5 - 2$)."
        },
        "a": 1.35,
        "b": -0.75,
        "point_biserial": 0.42
    },
    {
        "skill_code": "NET_IP_ROUTING",
        "stem": "What is the network address for an IP address of `192.168.10.138` with a subnet mask of `255.255.255.192` (`/26`)?",
        "options": [
            {"id": "A", "text": "192.168.10.128", "is_distractor": False},
            {"id": "B", "text": "192.168.10.0", "is_distractor": True},
            {"id": "C", "text": "192.168.10.64", "is_distractor": True},
            {"id": "D", "text": "192.168.10.192", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Subnet mask 192 has block size $256 - 192 = 64$. Subnets start at: 0, 64, 128, 192. Since 138 falls between 128 and 191, the network address is `192.168.10.128` (bitwise AND: $138 \\ \& \\ 192 = 128$).",
        "distractor_explanations": {
            "B": "The .0 subnet covers 0 to 63.",
            "C": "The .64 subnet covers 64 to 127.",
            "D": "192 is the start of the next subnet."
        },
        "a": 1.45,
        "b": 0.05,
        "point_biserial": 0.44
    },
    {
        "skill_code": "NET_IP_ROUTING",
        "stem": "Which routing algorithm rule determines how a router selects the matching route from its routing table when multiple prefix matches exist?",
        "options": [
            {"id": "A", "text": "Longest Prefix Match (LPM)", "is_distractor": False},
            {"id": "B", "text": "Shortest Prefix Match", "is_distractor": True},
            {"id": "C", "text": "Lowest Next-Hop IP value", "is_distractor": True},
            {"id": "D", "text": "First Alphabetical Interface", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Routers use the Longest Prefix Match principle: the route with the most specific (longest) subnet mask matching the destination IP address is selected.",
        "distractor_explanations": {
            "B": "Shortest prefix match is the default gateway `/0`, which is the fallback of last resort.",
            "C": "Next-hop value is arbitrary and not a routing selection criterion.",
            "D": "Interfaces are selected based on metric and prefix match, not alphabetical order."
        },
        "a": 1.50,
        "b": 0.35,
        "point_biserial": 0.45
    },
    {
        "skill_code": "NET_IP_ROUTING",
        "stem": "What is the primary protocol used to exchange routing reachability information **between different Autonomous Systems (AS)** on the global Internet?",
        "options": [
            {"id": "A", "text": "Border Gateway Protocol (BGP)", "is_distractor": False},
            {"id": "B", "text": "Open Shortest Path First (OSPF)", "is_distractor": True},
            {"id": "C", "text": "Routing Information Protocol (RIP)", "is_distractor": True},
            {"id": "D", "text": "Internet Control Message Protocol (ICMP)", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "BGP is the standardized Exterior Gateway Protocol (EGP) of the global Internet, routing between ISPs and autonomous systems using path-vector logic.",
        "distractor_explanations": {
            "B": "OSPF is an Interior Gateway Protocol (IGP) used within a single enterprise network.",
            "C": "RIP is an older distance-vector IGP.",
            "D": "ICMP handles error reporting (like ping and traceroute), not routing tables."
        },
        "a": 1.40,
        "b": -0.30,
        "point_biserial": 0.43
    },
    {
        "skill_code": "NET_IP_ROUTING",
        "stem": "What is the function of the **Time to Live (TTL)** field in an IPv4 header (or Hop Limit in IPv6)?",
        "options": [
            {"id": "A", "text": "It is decremented by 1 at each router hop to prevent packets from looping endlessly in the network.", "is_distractor": False},
            {"id": "B", "text": "It tracks the total latency in milliseconds since the packet was sent.", "is_distractor": True},
            {"id": "C", "text": "It defines when the cache entry in DNS expires.", "is_distractor": True},
            {"id": "D", "text": "It sets the connection timeout for TCP sockets.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "If a routing loop occurs, TTL prevents packets from circulating indefinitely. Each router decrements TTL; when it reaches 0, the packet is dropped and an ICMP Time Exceeded message is returned.",
        "distractor_explanations": {
            "B": "TTL is hop count, not clock elapsed time in milliseconds.",
            "C": "DNS TTL is for caching, distinct from the IP packet header TTL byte.",
            "D": "TCP socket timeout is controlled by OS kernel timers."
        },
        "a": 1.35,
        "b": -0.90,
        "point_biserial": 0.41
    },
    {
        "skill_code": "NET_IP_ROUTING",
        "stem": "Which IPv6 address is the exact equivalent of the IPv4 loopback address `127.0.0.1`?",
        "options": [
            {"id": "A", "text": "::1", "is_distractor": False},
            {"id": "B", "text": "::", "is_distractor": True},
            {"id": "C", "text": "fe80::1", "is_distractor": True},
            {"id": "D", "text": "ff02::1", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "In IPv6, the loopback address is written as `0000:0000:0000:0000:0000:0000:0000:0001` or compactly as `::1`.",
        "distractor_explanations": {
            "B": "`::` is the unspecified address (equivalent to 0.0.0.0 in IPv4).",
            "C": "`fe80::` represents link-local unicast addresses.",
            "D": "`ff02::1` is the all-nodes multicast address."
        },
        "a": 1.45,
        "b": 0.15,
        "point_biserial": 0.44
    },
    {
        "skill_code": "NET_IP_ROUTING",
        "stem": "In Network Address Translation (NAT) / Port Address Translation (PAT), how can hundreds of internal private hosts share a single public IPv4 address simultaneously?",
        "options": [
            {"id": "A", "text": "The router maps each internal IP and private port tuple to the public IP with a unique ephemeral Layer 4 port number in its state table.", "is_distractor": False},
            {"id": "B", "text": "By executing a round-robin schedule where only one computer can access the web per second.", "is_distractor": True},
            {"id": "C", "text": "By appending the private IP to the HTTP payload.", "is_distractor": True},
            {"id": "D", "text": "By generating MAC address collisions.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "PAT (NAPT) rewrites the source IP to the public IP and allocates a distinct source port (e.g., 50001, 50002). Incoming replies match the port number in the NAT translation table to route back to the correct private client.",
        "distractor_explanations": {
            "B": "Communications occur concurrently in parallel, not sequential time sharing.",
            "C": "Transport layer ports are translated, not HTTP application payloads.",
            "D": "MAC addresses are local to the LAN and not transmitted over the public Internet."
        },
        "a": 1.55,
        "b": 0.70,
        "point_biserial": 0.47
    }
]
