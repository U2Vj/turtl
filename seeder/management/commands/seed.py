from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand

from authentication.models import User
from catalog.models import Classroom, ClassroomInstructor, Project, Question, Task, QuestionChoice, AcceptanceCriteria, \
    HelpfulResource
from enrollments.models import Enrollment


def ask_question(question: str):
    result = input(f'{question} [yes|no] ')
    while len(result) < 1 or result[0].lower() not in "yn":
        result = input("Please answer yes or no: ")
    return result[0].lower() == "y"


class Command(BaseCommand):
    help = ("Seeds some test users, classrooms and enrollments into the database. "
            "Only intended for development purposes.")

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-input",
            "--noinput",
            action="store_true",
            help="Disables all confirmation prompts when seeding and flushing the database. Executes the default "
                 "'flush' command that Django provides."
        )

    def handle(self, *args, **options):
        if options["no_input"]:
            confirmation = True
        else:
            confirmation = ask_question("This command will seed multiple users, classrooms and enrollments into the "
                                        "database. It is intended for development purposes only. Using it in "
                                        "production can be dangerous.\n\nDo you want to continue?")

        if confirmation:
            print("Started seeding users...")

            # Hashed passwords
            hashed_student_password = make_password('student')
            hashed_instructor_password = make_password('instructor')
            hashed_admin_password = make_password('admin')

            # Create test students
            student1 = User.objects.create(email='student@localhost', username='TestStudent 1',
                                           password=hashed_student_password, role='STUDENT')
            student2 = User.objects.create(email='student2@localhost', username='TestStudent 2',
                                           password=hashed_student_password, role='STUDENT')
            student3 = User.objects.create(email='student3@localhost', password=hashed_student_password, role='STUDENT')
            student4 = User.objects.create(email='student4@localhost', password=hashed_student_password, role='STUDENT')
            student5 = User.objects.create(email='student5@localhost', password=hashed_student_password, role='STUDENT')

            # Create test instructors
            instructor1 = User.objects.create(
                email='instructor@localhost',
                username='TestInstructor 1',
                password=hashed_instructor_password,
                role='INSTRUCTOR'
            )
            instructor2 = User.objects.create(email='instructor2@localhost', username='TestInstructor 2',
                                              password=hashed_instructor_password, role='INSTRUCTOR')
            instructor3 = User.objects.create(email='instructor3@localhost', password=hashed_instructor_password,
                                              role='INSTRUCTOR')

            # Create test administrator
            administrator = User.objects.create(email='admin@localhost', username='TestAdministrator',
                                                password=hashed_admin_password, role='ADMINISTRATOR')

            print("Finished seeding users.")

            print("Started seeding classrooms...")

            # Create test classrooms
            computer_networks = Classroom.objects.create(title='Computer Networks')

            # Add instructors to classrooms
            ClassroomInstructor.objects.create(classroom=computer_networks, instructor=instructor2,
                                               added_by=instructor2)
            ClassroomInstructor.objects.create(classroom=computer_networks, instructor=instructor3,
                                               added_by=instructor2)
            ClassroomInstructor.objects.create(classroom=computer_networks, instructor=instructor1,
                                               added_by=instructor3)
            ClassroomInstructor.objects.create(classroom=computer_networks, instructor=administrator,
                                               added_by=instructor2)

            HelpfulResource.objects.create(
                title='The 5 different types of firewalls explained',
                url='https://www.techtarget.com/searchsecurity/feature/The-five-different-types-of-firewalls',
                classroom=computer_networks
            )
            HelpfulResource.objects.create(
                title='Tutorial: How To Set Up a Firewall with UFW on Ubuntu 22.04',
                url='https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-22-04',
                classroom=computer_networks
            )


            print("Finished seeding classrooms.")

            print("Started seeding projects...")

            # Create test projects
            firewalls = Project.objects.create(title='Web Security: Firewalls',
                                               classroom=computer_networks)
            cryptography_with_https = Project.objects.create(title='Cryptography with HTTPS',
                                                             classroom=computer_networks)
            # TASKS: intro, securing an nginx web server
            dns = Project.objects.create(title='DNS',
                                         classroom=computer_networks)
            # TASKS: What is the DNS and what is it used for?, Sending a DNS request using the Linux terminal

            print("Finished seeding projects.")

            print("Started seeding tasks...")

            # Create test tasks

            # TASK 1: Introduction to Firewalls
            introduction_firewalls_question1 = Question.objects.create(
                question='What is the primary purpose of a firewall?',
                question_type='SINGLE_CHOICE'
            )
            QuestionChoice.objects.create(answer='To enhance internet speed', question=introduction_firewalls_question1,
                                          is_correct=False)
            QuestionChoice.objects.create(answer='To monitor and control network access',
                                          question=introduction_firewalls_question1, is_correct=True)
            QuestionChoice.objects.create(answer='To design graphical user interfaces',
                                          question=introduction_firewalls_question1, is_correct=False)
            QuestionChoice.objects.create(answer='To manage hardware resources',
                                          question=introduction_firewalls_question1, is_correct=False)
            introduction_firewalls_question2 = Question.objects.create(
                question='Which layer of the OSI model do proxy firewalls operate at?',
                question_type='SINGLE_CHOICE'
            )
            QuestionChoice.objects.create(answer='Network layer (Layer 3)', question=introduction_firewalls_question2,
                                          is_correct=False)
            QuestionChoice.objects.create(answer='Transport layer (Layer 4)', question=introduction_firewalls_question2,
                                          is_correct=False)
            QuestionChoice.objects.create(answer='Application layer (Layer 7)',
                                          question=introduction_firewalls_question2, is_correct=True)
            QuestionChoice.objects.create(answer='Data link layer (Layer 2)', question=introduction_firewalls_question2,
                                          is_correct=False)
            introduction_firewalls_question3 = Question.objects.create(
                question='What are the key features of Next-Generation Firewalls for advanced security?',
                question_type='MULTIPLE_CHOICE'
            )
            QuestionChoice.objects.create(answer='Deep packet inspection', question=introduction_firewalls_question3,
                                          is_correct=True)
            QuestionChoice.objects.create(answer='Operating only at the network layer',
                                          question=introduction_firewalls_question3, is_correct=False)
            QuestionChoice.objects.create(answer='Incorporating intrusion detection and prevention systems',
                                          question=introduction_firewalls_question3, is_correct=True)
            QuestionChoice.objects.create(answer='Securing network access with a password',
                                          question=introduction_firewalls_question3, is_correct=False)

            introduction_firewalls_acceptance_criteria = AcceptanceCriteria.objects.create(criteria_type='QUIZ')
            introduction_firewalls_acceptance_criteria.questions.add(introduction_firewalls_question1)
            introduction_firewalls_acceptance_criteria.questions.add(introduction_firewalls_question2)
            introduction_firewalls_acceptance_criteria.questions.add(introduction_firewalls_question3)

            Task.objects.create(
                title='Introduction',
                description="In the vast expanse of the internet, the need for robust security measures is paramount. "
                            "At the forefront of digital defense stands the firewall, a virtual sentinel that plays a "
                            "pivotal role in safeguarding networks. To comprehend its significance, one must delve "
                            "into what firewalls are, how they function, and the diverse applications they serve in "
                            "the modern digital landscape.\n\nAt its core, a firewall is a security system that "
                            "monitors and controls incoming and outgoing network traffic. It acts as a barrier between "
                            "a trusted internal network and untrusted external networks, such as the internet. The "
                            "primary objective is to establish a protective barrier, scrutinizing data packets as they "
                            "traverse the network and making decisions based on predetermined security rules.\n\n"
                            "Firewalls come in various forms, each tailored to address specific security requirements:"
                            "\n\nPacket Filtering Firewalls:\nOperate at the network layer (Layer 3) and make "
                            "decisions based on predefined rules for individual data packets\n\nStateful Inspection "
                            "Firewalls:\nAlso at the network layer, these firewalls not only examine each packet, but "
                            "also keep track of whether or not that packet is part of an established TCP or other "
                            "network session.\n\nProxy Firewalls:\nOperate at the application layer (Layer 7) and act "
                            "as intermediaries, inspecting and filtering traffic not just using the address, port and "
                            "TCP header information, but also the application-specific content itself. This is why "
                            "they are sometimes also referred to as Application-level gateways.\n\nNext-Generation "
                            "Firewalls:\nCombining features of traditional firewalls with advanced security "
                            "technologies, these firewalls operate at multiple layers. In addition to packet "
                            "inspection with stateful inspection, they can incorporate intrusion detection and "
                            "prevention systems, deep packet inspection and malware filtering.\n\nThe main purpose of "
                            "firewalls is access control: Firewalls regulate access to a network by enforcing "
                            "predefined rules. Unauthorized access attempts are thwarted, ensuring that only "
                            "legitimate traffic is allowed. Firewalls can also be used to maintain detailed logs of "
                            "network activity, facilitating the identification of potential security incidents, with "
                            "monitoring tools providing real-time insights.",
                task_type='NEUTRAL',
                difficulty='BEGINNER',
                project=firewalls,
                acceptance_criteria=introduction_firewalls_acceptance_criteria
            )

            # TASK 2: How To Set Up a Firewall with UFW
            ufw_firewall_question = Question.objects.create(
                question='What does the acronym UFW stand for?',
                question_type='SINGLE_CHOICE'
            )
            QuestionChoice.objects.create(answer='Uncommon Firewall', question=ufw_firewall_question,
                                          is_correct=False)
            QuestionChoice.objects.create(answer='Uncomplicated Firewall',
                                          question=ufw_firewall_question, is_correct=True)
            QuestionChoice.objects.create(answer='Unix Firewall',
                                          question=ufw_firewall_question, is_correct=False)

            ufw_firewall_acceptance_criteria = AcceptanceCriteria.objects.create(criteria_type='QUIZ')
            ufw_firewall_acceptance_criteria.questions.add(ufw_firewall_question)

            Task.objects.create(
                title='Firewalls with UFW',
                description="The Uncomplicated Firewall (UFW) is a user-friendly front-end for managing iptables, the "
                            "default firewall management tool for Linux. Designed for simplicity, UFW allows users to "
                            "easily configure and control firewall settings through a command-line interface, "
                            "providing an efficient means to secure and manage network traffic on Linux systems. In "
                            "this guide, you will secure an Ubuntu server with the UFW and learn how to easily block "
                            "traffic on certain ports.\n\n1. SSH into the server\nServers are usually accessed "
                            "remotely via SSH. To access the server in this task's virtual environment, type the "
                            "following command into the terminal on the right-hand side:\n\nssh "
                            "default@ADD_IPADDRESS\n\nThe password for the default user is: turtl\n\n"
                            "2. Update the package repositories\nUbuntu maintains a list of packages (i.e. programs). "
                            "These packages can be installed using the package manager APT. To ensure that you "
                            "install the latest version of the UFW, please update the package repositories using:\n\n"
                            "sudo apt update\n\n3. Install the UFW\n\nsudo apt install -y ufw\n\n4. Setting up default "
                            "policies\nIf you are setting up a firewall, the rules you will most likely begin with are "
                            "the default rules. They will be followed if no other, more specific rule applies. "
                            "Usually, it is a good idea to deny every incoming traffic (meaning every traffic from the "
                            "outside cannot reach the server) and allow every outgoing traffic (meaning services "
                            "running on the server itself can still reach the outside network). Remember: There will "
                            "be more specific rules that are exceptions to this, but as a default, this is a good "
                            "starting point. To set up these rules, type in:\n\nsudo ufw default deny incoming\nsudo "
                            "ufw default allow outgoing\n\n5. Allow certain services:\nIf you were to enable the "
                            "firewall now, no traffic from outside could reach the server, including the SSH "
                            "connection you are using to connect to the Ubuntu server. Consequently, it makes sense to "
                            "allow SSH connections:\n\nsudo ufw allow ssh\n\nCheck the changes you have made by "
                            "running:\n\nsudo ufw status\n\nFor a real-world example, imagine you are running a web "
                            "server on port 80 (HTTP) and 443 (HTTPS). To allow traffic to reach the web server, "
                            "execute:\n\nsudo ufw allow http\nsudo ufw allow https\n\nYou can alternatively specify "
                            "the port number instead:\n\nsudo ufw allow 80\nsudo ufw allow 443\n\n6. Enable the "
                            "firewall\nTo enable the firewall you just configured, run the following command:\n\nsudo "
                            "ufw enable\n\nYou should now have a working firewall!\n\n7. Test the firewall using "
                            "nmap\nNow, you can test your newly configured firewall. To do this, exit the SSH session "
                            "and leave your server by entering:\n\nexit\n\nNext, run a port scan using nmap:\n\n"
                            "nmap -sS ADD_IPADDRESS\n\nPlease note: Running a port scan against infrastructure that "
                            "you do not own or are allowed to test might be illegal.\n\nIf all goes well, the only "
                            "open ports should be port 22 (SSH), port 80 (HTTP) and port 443 (HTTPS).",
                task_type='DEFENSE',
                difficulty='BEGINNER',
                project=firewalls,
                acceptance_criteria=ufw_firewall_acceptance_criteria
            )

            # TASK: What is HTTPS?

            introduction_https_question1 = Question.objects.create(
                question='What is the primary purpose of HTTPS?',
                question_type='SINGLE_CHOICE'
            )
            QuestionChoice.objects.create(answer='Enhancing website aesthetics', question=introduction_https_question1,
                                          is_correct=False)
            QuestionChoice.objects.create(answer='Speeding up internet connections',
                                          question=introduction_https_question1, is_correct=False)
            QuestionChoice.objects.create(answer='Securing data communication on the web',
                                          question=introduction_https_question1, is_correct=True)
            QuestionChoice.objects.create(answer='Creating user-friendly interfaces',
                                          question=introduction_https_question1, is_correct=False)
            introduction_https_question2 = Question.objects.create(
                question='During the TLS handshake, what is established between the client and server?',
                question_type='SINGLE_CHOICE'
            )
            QuestionChoice.objects.create(answer='Social connection', question=introduction_https_question2,
                                          is_correct=False)
            QuestionChoice.objects.create(answer='Encryption algorithms and keys',
                                          question=introduction_https_question2, is_correct=True)
            QuestionChoice.objects.create(answer='Internet speed parameters',
                                          question=introduction_https_question2, is_correct=False)
            QuestionChoice.objects.create(answer='Graphic design preferences', question=introduction_https_question2,
                                          is_correct=False)
            introduction_https_question3 = Question.objects.create(
                question='What are the key components of the TLS handshake in HTTPS?',
                question_type='MULTIPLE_CHOICE'
            )
            QuestionChoice.objects.create(answer='Negotiation of encryption algorithms',
                                          question=introduction_https_question3, is_correct=True)
            QuestionChoice.objects.create(answer='Exchange of cryptographic keys',
                                          question=introduction_https_question3, is_correct=True)
            QuestionChoice.objects.create(answer='Verification of web server identity',
                                          question=introduction_https_question3, is_correct=True)
            QuestionChoice.objects.create(answer='Compression of data during transmission',
                                          question=introduction_https_question3, is_correct=False)

            introduction_https_acceptance_criteria = AcceptanceCriteria.objects.create(criteria_type='QUIZ')
            introduction_https_acceptance_criteria.questions.add(introduction_https_question1)
            introduction_https_acceptance_criteria.questions.add(introduction_https_question2)
            introduction_https_acceptance_criteria.questions.add(introduction_https_question3)

            Task.objects.create(
                title='What is HTTPS?',
                description="In the vast landscape of the internet, where information flows ceaselessly, ensuring the "
                            "security and privacy of data exchanged between users and websites is paramount. Hypertext "
                            "Transfer Protocol Secure (HTTPS) stands as a robust safeguard, providing a secure "
                            "communication channel over the inherently vulnerable medium of the World Wide Web. "
                            "This protocol is a cornerstone in the realm of web security, employing a combination of "
                            "encryption, authentication, and integrity mechanisms to fortify data transmissions and "
                            "protect users from various cyber threats.\n\nHTTPS, the secure counterpart to HTTP, "
                            "evolved as a response to the growing need for secure online transactions and data "
                            "exchange. HTTP, the foundation of data communication on the web, lacked the encryption "
                            "features necessary to shield sensitive information from eavesdroppers and malicious "
                            "actors. HTTPS addresses this vulnerability by integrating the Transport Layer Security "
                            "(TLS) or its predecessor, the Secure Sockets Layer (SSL) protocols, into the "
                            "communication process.\n\nThe encryption mechanism employed by HTTPS plays a pivotal role "
                            "in safeguarding data during transit. When a user initiates a connection to an "
                            "HTTPS-enabled website, a process known as the TLS handshake ensues. During this "
                            "handshake, the client and server establish a secure communication channel by negotiating "
                            "encryption algorithms and exchanging cryptographic keys. This ensures that any data "
                            "transmitted between the user's device and the web server remains confidential, rendering "
                            "it nearly impossible for unauthorized entities to intercept or decipher.\n\nBeyond "
                            "encryption, HTTPS incorporates authentication mechanisms to verify the legitimacy of the "
                            "web server. This is crucial in preventing man-in-the-middle attacks where a malicious "
                            "entity intercepts and alters the communication between the user and the server. "
                            "Certificates, specifically X.509 digital certificates, play a central role in this "
                            "authentication process. Web servers obtain these certificates from trusted Certificate "
                            "Authorities (CAs), which act as digital notaries, verifying the legitimacy of the "
                            "server's identity. When a user connects to an HTTPS-enabled site, the browser checks the "
                            "server's certificate to ensure it is valid and issued by a trusted CA, establishing trust "
                            "in the authenticity of the website.\n\nIntegrity, the third pillar of HTTPS, ensures that "
                            "the data exchanged between the client and server remains unchanged during transit. This "
                            "is achieved through the use of cryptographic hash functions, which generate unique "
                            "checksums for the transmitted data. The recipient can then verify the integrity of the "
                            "received data by comparing the checksum with the original hash value.\n\nHTTPS has become "
                            "a non-negotiable standard for websites, particularly those handling sensitive information "
                            "such as login credentials, personal details, and financial transactions. Major web "
                            "browsers have also taken strides to promote a secure online environment by flagging "
                            "non-HTTPS sites as \"Not Secure,\" nudging website owners to adopt HTTPS for the sake of "
                            "user trust.\n\nIn conclusion, HTTPS stands as the bedrock of secure web communication, "
                            "weaving together encryption, authentication, and integrity mechanisms to protect users "
                            "from the perils of the digital realm. As the internet continues to evolve, the adoption "
                            "of HTTPS remains a fundamental step towards fostering a secure and trustworthy online "
                            "experience for users worldwide.",
                task_type='NEUTRAL',
                difficulty='BEGINNER',
                project=cryptography_with_https,
                acceptance_criteria=introduction_https_acceptance_criteria
            )

            print("Finished seeding tasks.")

            print("Started seeding enrollments...")

            Enrollment.objects.create(classroom=computer_networks, student=student1)
            Enrollment.objects.create(classroom=computer_networks, student=student2)
            Enrollment.objects.create(classroom=computer_networks, student=student3)
            Enrollment.objects.create(classroom=computer_networks, student=instructor1)
            Enrollment.objects.create(classroom=computer_networks, student=instructor2)
            Enrollment.objects.create(classroom=computer_networks, student=administrator)

            print("Finished seeding enrollments.")
            print("Finished seeding the database.")
