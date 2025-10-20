# Author: Claude Code
# Released under Gnu GPL v2.0, see LICENSE file for details
"""Generate Mermaid sequence diagrams from TLS conversation trees"""

from __future__ import print_function

from tlslite.constants import ContentType, HandshakeType, AlertLevel, \
        AlertDescription, SSL2HandshakeType, ExtensionType
from tlsfuzzer.expect import ExpectClose, ExpectNoMessage, ExpectAlert
from tlsfuzzer.runner import guess_response


INDENT = "    "

class Visualizer(object):
    """Generate Mermaid sequence diagram from a conversation"""

    def __init__(self, conversation):
        """Link conversation with visualizer"""
        self.conversation = conversation
        self.diagram_lines = []
        self.tcp_buffering_active = False

    @staticmethod
    def _format_extensions(node):
        """Format extensions list from a node if available.

        Returns a list of extension names, or None if no extensions.
        """
        if not hasattr(node, 'extensions') or not node.extensions:
            return None

        # For expect nodes, extensions is a dict
        if isinstance(node.extensions, dict):
            ext_list = [ExtensionType.toStr(ext_id)
                       for ext_id in node.extensions.keys()]
        # For generator nodes with a list
        elif hasattr(node.extensions, '__iter__'):
            ext_list = [ExtensionType.toStr(ext_id)
                       for ext_id in node.extensions]
        else:
            return None

        if ext_list:
            return ext_list
        return None

    def _add_extension_note(self, node, sender="Client", depth=0):
        """Add a note box with extensions if the node has any.

        Args:
            node: The node to check for extensions
            sender: The sender of the message ("Client" or "Server")
            depth: Indentation depth
        """
        ext_list = self._format_extensions(node)
        if ext_list:
            ext_text = "<br/>".join(ext_list)
            if sender == "Client":
                position = "left of Client"
            else:
                position = "right of Server"
            self.diagram_lines.append(f"{INDENT*depth}Note {position}: {ext_text}")

    def draw_node(self, node, depth):
        if node.is_command():
            # Commands are internal operations, usually not shown
            # but we can show Connect and Close operations
            command_result = self._describe_command(node)
            command_desc, command_type = command_result

            if command_type == 'tcp_buffering_enable':
                self.diagram_lines.append(f"{INDENT*depth}activate Client")
                self.tcp_buffering_active = True
            elif command_type == 'tcp_buffering_disable':
                if self.tcp_buffering_active:
                    self.diagram_lines.append(f"{INDENT*depth}deactivate Client")
                    self.tcp_buffering_active = False

            if command_desc:
                self.diagram_lines.append(f"{INDENT*depth}Note over Client: {command_desc}")

        elif node.is_expect():
            # This is an expectation of receiving a message from server
            expect_desc = self._describe_expect(node)
            if expect_desc:
                if isinstance(node, ExpectClose):
                    self.diagram_lines.append(f"{INDENT*depth}Server-->>Client: {expect_desc}")
                elif not isinstance(node, ExpectNoMessage):
                    self.diagram_lines.append(f"{INDENT*depth}Server->>Client: {expect_desc}")
                self._add_extension_note(node, sender="Server")

        elif node.is_generator():
            # This is a message generator - client sending to server
            gen_desc = self._describe_generator(node)
            if gen_desc:
                self.diagram_lines.append(f"{INDENT*depth}Client->>Server: {gen_desc}")
            self._add_extension_note(node, sender="Client")

        else:
            # Unknown node type, skip it
            pass


    def walk(self, node, depth):
        while node is not None:
            if node.child == node:
                self.diagram_lines.append(f"{INDENT*depth}loop")
                self.draw_node(node, depth + 1)
                self.diagram_lines.append(f"{INDENT*depth}end")
                node = node.next_sibling
                continue

            elif node.next_sibling is not None:
                self.diagram_lines.append(f"{INDENT*depth}alt")
                sibling = node.next_sibling
                while sibling is not None:
                    next_sibling = sibling.next_sibling
                    sibling.next_sibling = None
                    self.walk(sibling, depth + 1)
                    if next_sibling:
                        self.diagram_lines.append(f"{INDENT*depth}else")
                    sibling = next_sibling
                self.diagram_lines.append(f"{INDENT*depth}end")

            else:
                self.draw_node(node, depth)

            node = node.child
                

    def generate(self):
        """Generate Mermaid sequence diagram from conversation"""
        self.diagram_lines = []
        self.tcp_buffering_active = False
        self.diagram_lines.append("sequenceDiagram")
        self.diagram_lines.append("    participant Client")
        self.diagram_lines.append("    participant Server")

        # Walk through the conversation tree
        node = self.conversation
        self.walk(node, 1)

        return "\n".join(self.diagram_lines)

    def _describe_command(self, node):
        """Generate description for a command node

        Returns a tuple: (description, command_type)
        - description: String to display, or None to skip
        - command_type: 'tcp_buffering_enable', 'tcp_buffering_flush',
                       'tcp_buffering_disable', or None
        """
        class_name = node.__class__.__name__

        if class_name == "Connect":
            return (f"Connect to {node.hostname}:{node.port}", None)
        elif class_name == "Close":
            return ("Close connection", None)
        elif class_name == "ResetHandshakeHashes":
            return ("Reset handshake hashes", None)
        elif class_name == "SetRecordVersion":
            return (f"Set record version to {node.version}", None)
        elif class_name == "TCPBufferingEnable":
            return (None, 'tcp_buffering_enable')
        elif class_name == "TCPBufferingFlush":
            return ("Flush buffered data", 'tcp_buffering_flush')
        elif class_name == "TCPBufferingDisable":
            return (None, 'tcp_buffering_disable')
        # Most other commands are internal state changes, don't show them
        return (None, None)

    def _describe_expect(self, node):
        """Generate description for an expect node"""
        class_name = node.__class__.__name__

        if isinstance(node, ExpectClose):
            return "Connection closed"
        elif isinstance(node, ExpectNoMessage):
            return None  # Don't show timeout expectations
        elif isinstance(node, ExpectAlert):
            level_str = ""
            desc_str = ""
            if hasattr(node, 'level') and node.level is not None:
                level_str = AlertLevel.toStr(node.level)
            if hasattr(node, 'description') and node.description is not None:
                if isinstance(node.description, (list, tuple)):
                    desc_str = "/".join(AlertDescription.toStr(d) for d in node.description)
                else:
                    desc_str = AlertDescription.toStr(node.description)

            if level_str and desc_str:
                return f"Alert({level_str}, {desc_str})"
            elif desc_str:
                return f"Alert({desc_str})"
            elif level_str:
                return f"Alert({level_str})"
            else:
                return "Alert"

        # For handshake messages
        if class_name == "ExpectServerHello":
            return "ServerHello"
        elif class_name == "ExpectServerHello2":
            return "ServerHello (SSLv2)"
        elif class_name == "ExpectHelloRetryRequest":
            return "HelloRetryRequest"
        elif class_name == "ExpectCertificate":
            return "Certificate"
        elif class_name == "ExpectCompressedCertificate":
            return "CompressedCertificate"
        elif class_name == "ExpectCertificateVerify":
            return "CertificateVerify"
        elif class_name == "ExpectServerKeyExchange":
            return "ServerKeyExchange"
        elif class_name == "ExpectCertificateRequest":
            return "CertificateRequest"
        elif class_name == "ExpectServerHelloDone":
            return "ServerHelloDone"
        elif class_name == "ExpectChangeCipherSpec":
            return "ChangeCipherSpec"
        elif class_name == "ExpectFinished":
            return "Finished"
        elif class_name == "ExpectEncryptedExtensions":
            return "EncryptedExtensions"
        elif class_name == "ExpectNewSessionTicket":
            return "NewSessionTicket"
        elif class_name == "ExpectHelloRequest":
            return "HelloRequest"
        elif class_name == "ExpectApplicationData":
            return "ApplicationData"
        elif class_name == "ExpectHeartbeat":
            return "Heartbeat"
        elif class_name == "ExpectCertificateStatus":
            return "CertificateStatus"
        elif class_name == "ExpectKeyUpdate":
            return "KeyUpdate"
        elif class_name == "ExpectVerify":
            return "Verify (SSLv2)"
        elif class_name == "ExpectSSL2Alert":
            return "Alert (SSLv2)"

        # Generic fallback
        if class_name.startswith("Expect"):
            return class_name[6:]  # Remove "Expect" prefix
        return class_name

    def _describe_generator(self, node):
        """Generate description for a generator node"""
        class_name = node.__class__.__name__

        if class_name == "ClientHelloGenerator":
            return "ClientHello"
        elif class_name == "ClientKeyExchangeGenerator":
            return "ClientKeyExchange"
        elif class_name == "ClientMasterKeyGenerator":
            return "ClientMasterKey (SSLv2)"
        elif class_name == "CertificateGenerator":
            return "Certificate"
        elif class_name == "CompressedCertificateGenerator":
            return "CompressedCertificate"
        elif class_name == "CertificateVerifyGenerator":
            return "CertificateVerify"
        elif class_name == "ChangeCipherSpecGenerator":
            return "ChangeCipherSpec"
        elif class_name == "FinishedGenerator":
            return "Finished"
        elif class_name == "AlertGenerator":
            level_str = ""
            desc_str = ""
            if hasattr(node, 'level') and node.level is not None:
                level_str = AlertLevel.toStr(node.level)
            if hasattr(node, 'description') and node.description is not None:
                desc_str = AlertDescription.toStr(node.description)

            if level_str and desc_str:
                return f"Alert({level_str}, {desc_str})"
            elif desc_str:
                return f"Alert({desc_str})"
            else:
                return "Alert"
        elif class_name == "ApplicationDataGenerator":
            return "ApplicationData"
        elif class_name == "HeartbeatGenerator":
            return "Heartbeat"
        elif class_name == "KeyUpdateGenerator":
            return "KeyUpdate"
        elif class_name == "RawMessageGenerator":
            if hasattr(node, 'description') and node.description:
                return f"RawMessage({node.description})"
            return "RawMessage"
        elif class_name == "PlaintextMessageGenerator":
            if hasattr(node, 'description') and node.description:
                return f"PlaintextMessage({node.description})"
            return "PlaintextMessage"
        elif class_name == "RawSocketWriteGenerator":
            if hasattr(node, 'description') and node.description:
                return f"RawSocketWrite({node.description})"
            return "RawSocketWrite"
        elif class_name == "PopMessageFromList":
            return "Message (from list)"
        elif class_name == "FlushMessageList":
            return "Flush message list"

        # Generic fallback
        if class_name.endswith("Generator"):
            return class_name[:-9]  # Remove "Generator" suffix
        return class_name
