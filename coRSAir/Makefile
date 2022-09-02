INC     =   /Users/agalan-h/.brew/opt/openssl@1.1/include
LIB     =   /Users/agalan-h/.brew/opt/openssl@1.1/lib
CFLAGS  =   -Werror -Wall -Wextra

all: 
	@clear
	gcc corsair.c $(CFLAGS) -I$(INC) -L$(LIB) -lssl -lcrypto -o corsair
	@./corsair ./Recursos/cert1.pem ./Recursos/cert2.pem ./Recursos/passwd.enc
