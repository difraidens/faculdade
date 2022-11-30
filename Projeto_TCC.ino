#include <Boards.h>
#include <Firmata.h>
#include <FirmataConstants.h>
#include <FirmataDefines.h>
#include <FirmataMarshaller.h>
#include <FirmataParser.h>



/* ======================================================================================================

   HARDWARE:

   ARDUINO   SENSOR DE TENSÃO
   GND           GND
   A0            S


   ARDUINO    DISPLAY I2C

   GND          GND
   5V           VCC
   A4           SDA
   A5           SCL

   ARDUINO    RELÉ
   8           IN
   5V          VCC
   GND         GND
              
====================================================================================================== */


// ======================================================================================================
// --- Bibliotecas Auxiliares ---
#include <Wire.h>
#include <LiquidCrystal_I2C.h>


// ======================================================================================================

// DEFINIÇÕES
#define endereco  0x27 // ENDEREÇO DO DISPLAY
#define colunas   16  // NUMERO DE COLUNAS DO DISPLAY
#define linhas    2   // NUMERO DE LINHAS DO DISPLAY

// INSTANCIANDO OBJETOS
LiquidCrystal_I2C lcd(endereco, colunas, linhas);
 

// ======================================================================================================
// --- Variáveis Globais ---
float volts = 0;
float mediaTensao = 0; // variavel para soma das medias
float MediaVolts = 0; //variavel para recerber o valor final de Volts
float RealVolts = 0; //variavel para recerber o valor final de Volts
int dado;
char cmd;


// ======================================================================================================
// --- Configurações Iniciais ---
void setup()
{
    // DISPLAY
     lcd.init(); // INICIA A COMUNICAÇÃO COM O DISPLAY
     lcd.backlight(); // LIGA A ILUMINAÇÃO DO DISPLAY
     lcd.clear(); // LIMPA O DISPLAY
     lcd.setCursor(0,0);
     lcd.print("   INICIANDO   ");

    //MONITOR SERIAL
     Serial.begin(9600);

    // RELÉ
     pinMode (8, OUTPUT); //DEFININDO O PINO 8 COMO SAIDA (RELÉ)
     digitalWrite(8,HIGH); //DEFININDO RELÉ PRA COMEÇAR DESLIGADO
 
} //end setup
 

// --- Loop Infinito ---
void loop()
{

   mediaTensao = 0;
   for (int j = 0; j < 18 ; j++){
   for (int i = 0; i < 1000 ; i++) {// repete por 1000 vezes para der uma precisão melhor
    volts = analogRead(0)*(5.0/1023.0);;//recebe o valor do sensor que vai de 0 até 1023
    volts = (volts*5.0); //calcula o valor com base na configuração do sensor
    mediaTensao = mediaTensao + volts; //faz o calculo matematico
    delay(10);
   }
        delay(600000);
   }

  MediaVolts = mediaTensao / 1000; //calcula a media dos valores

   Serial.println(MediaVolts);
   // EXIBIR NO DISPLAY OS DADOS 
   lcd.setCursor(0,0);
   lcd.print("   Voltimetro   ");
   lcd.setCursor(5,1);
   lcd.print(MediaVolts);
   lcd.setCursor(9,1);
   lcd.print(" V");

	if(Serial.available()>0) {
		int dado = Serial.read();

		if (dado == '1'){
    digitalWrite(8,HIGH);
    delay(1);
    }
		else if (dado == '0'){
    digitalWrite(8, LOW);
    delay(1);
   }

  Serial.print("Valor: "); 
  Serial.print(MediaVolts);
  Serial.print(dado);
  Serial.println(" VOLTS");

   delay(2222);


  }
} //end loop
 

 





























