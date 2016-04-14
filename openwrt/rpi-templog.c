#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>

#include <resolv.h>
#include <netdb.h>

#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <arpa/inet.h>

#define MSGLEN 25

/* limit the lines so that show last 24 hours
 * one line is 1 minute, 60min*24h, plus 5 for error, 0 => offset + 5 c*/
#define MAXLINES (1445 + 5)
#define MAXOFF (MAXLINES * MSGLEN)

#define PORT 8000

const char *FILENAME = "/www/temp/temp.log";
const mode_t create_mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH;

int ctrl = 0;

void handle_sig(int signum)
{
	ctrl = 1;
}

struct sigaction int_handler = {
	.sa_handler = handle_sig,
};

void error_exit(char *msg)
{
	perror(msg);
	exit(errno);
}

inline void print_usage(const char *program_name)
{
	printf("\nUsage: %s [OPTIONS...]\n", program_name);
	printf("\n");
	printf("  -p port	server port that waits for the data.\n");
	printf("  -f file	file to save the data [WARNING CHANGE .html FILENAME].\n");
	printf("  -h     	prints this menu.\n\n");
}

int main(int argc, char *argv[])
{   
	socklen_t addrlen;
	char buffer[MSGLEN];
	unsigned int count = 5;
	const char *file_name = NULL;
	struct sockaddr_in serv_addr, cli_addr;
	int sockfd, clientfd, file, size, opt, port, p_flag = 0, f_flag = 0;

	errno = 0; /* set errno */

	while ((opt = getopt(argc, argv, "p:f:h")) != -1) {
        switch (opt) {
        case 'p':
            port = atoi(optarg);
            p_flag = 1;
            break;
        case 'f':
            file_name = optarg;
            f_flag = 1;
            break;
        case 'h':
            print_usage(argv[0]);
            exit(EXIT_SUCCESS);
            break;
        default: /* '?' */
            print_usage(argv[0]);
            exit(EXIT_FAILURE);
        }
    }
    
    if(!f_flag)
		file_name = FILENAME;
	if(!p_flag)
		port = PORT;

	file = open(file_name, O_RDWR);
	if(file == -1) {
		if(errno == ENOENT) {
			file = creat(file_name, create_mode);
			if(file == -1)
				error_exit("ERROR creating file");
			write(file, &count, sizeof(count)); /* start from beginning = 5*/
			write(file, "\n", strlen("\n"));
		}
		else
			error_exit("ERROR opening file");
	}

	/* assume success, raw data, where to start writing */
	lseek(file, 0, SEEK_SET);
	read(file, &count, sizeof(count));
	lseek(file, count, SEEK_SET);

	/* create streaming socket */
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
		error_exit("ERROR socket creating");
	
	/* setsockopt: Handy debugging trick that lets Eliminate ERROR on binding */
	opt = 1; /* reuse opt safe here */
	setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (const void *)&opt , sizeof(int));

	/* initialize address and port structure */
	bzero(&serv_addr, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(port);

	/* assign a port number to the socket usign bind */
    if (bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0)
		error_exit("ERROR socket binding");

	/* make listening socket */
	if (listen(sockfd, 2) != 0)
		error_exit("ERROR socket listening");

	while (1)
	{
		addrlen = sizeof(struct sockaddr_in);

		/* accept a connection to our client */
		clientfd = accept(sockfd, (struct sockaddr*)&cli_addr, &addrlen);
		if (clientfd < 0)
			error_exit("ERROR on accept");

		while (1)
		{
			bzero(buffer, MSGLEN);

			size = read(clientfd, buffer, MSGLEN);

			if(size == 0) /* error_exit("ERROR pipe broken, resolve and restart"); */
				break;

			if(size < 0)
				error_exit("ERROR reading from socket, resolve and restart");

			write(clientfd, buffer, size); /* assume success */

			if(write(file, buffer, size) != size)
				error_exit("ERROR writing, resolve and restart");

			if(count > MAXOFF) { /* reset offset, begin */
				count = 5;
				lseek(file, 0, SEEK_SET);
				write(file, &count, sizeof(count));
				lseek(file, count, SEEK_SET);
			}
			else { /* save current offset */
				lseek(file, 0, SEEK_SET);
				count += MSGLEN;
				write(file, &count, sizeof(count));
				lseek(file, count, SEEK_SET);
			}

			fsync(file); /* just to be sure */

			if(ctrl)
				break;
		}

		if(ctrl)
			break;
	}

	close(clientfd); /* close data connection */
	close(sockfd); /* close server */

	return 0;
}
