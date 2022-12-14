#include <Stepper.h>

#define STEP_COUNT 32

#define trigPin 3
#define echoPin 2

#define pinLeft1 10
#define pinLeft2 12
#define pinRight1 11
#define pinRight2 13

Stepper stepper(STEP_COUNT, pinLeft1, pinLeft2, pinRight1, pinRight2);

void setup()
{
    Serial.begin(9600);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);

    stepper.setSpeed(100);
}

int lastInputIndex = 0;
String lastCommand;

void loop()
{
    String input = Serial.readString();
    if(!input.equals("\n"))
    {
        String parsed_input = input.substring(0, input.indexOf('\n'));
        String command = parsed_input.substring(0, parsed_input.indexOf(' '));
        int wartosc = parsed_input.substring(parsed_input.indexOf(' '), parsed_input.length()).toInt();

        int odleglosc = 0;
        if(command.equals(String("rotate")))
        {
            Serial.println("Rotating...");
            rotate(wartosc);
        }
        if(command.equals(String("measure")))
        {
            odleglosc = measureDistance();
            Serial.println("distance: " + (String)odleglosc);
        }
        if(command.equals(String("speed")))
        {
            stepper.setSpeed(wartosc);
            Serial.println("New Speed = " + (String)wartosc);
        }
    }
}

int measureDistance()
{
    long czas, dystans;

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    czas = pulseIn(echoPin, HIGH);
    dystans = czas / 58;

    return dystans;
}

void rotate(int degrees)
{
    degrees %= 361;
    stepper.step(2048/360 * degrees);
}
