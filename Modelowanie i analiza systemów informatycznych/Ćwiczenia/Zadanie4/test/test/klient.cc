//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

#include "klient.h"
#include "wlasnyMsg_m.h"

Define_Module(Klient);

void Klient::initialize()
{
    cMessage *wlasnaWiadomosc = new cMessage();

    czasMiedzyZadaniamiSignal = registerSignal("czasMiedzyZadaniami");
    wielkoscZadaniaSignal = registerSignal("wielkoscZadania");

    scheduleAt(simTime(),wlasnaWiadomosc);


}

void Klient::handleMessage(cMessage *msg)
{
    WlasnyMsg *zadanie;
    if (msg->isSelfMessage())
    {
        zadanie = new WlasnyMsg();
        zadanie->setKind(2);
        zadanie->setName("Wiadomość");

        // Generowanie wielkości zadania z rozkładu normalnego
        int wielkoscZadania = int(normal(5000, sqrt(333)));
        if (wielkoscZadania < 100) wielkoscZadania = 100;  // Ograniczenie minimalne

        zadanie->setWielkoscZadania(wielkoscZadania);
        zadanie->setIdKlienta((int)par("idKlienta"));

        send(zadanie, "odDoPrzelacznika$o");

        double czasMiedzyZadaniami = (double)par("czasMiedzyZadaniami");
        scheduleAt(simTime() + czasMiedzyZadaniami, msg);

        simsignal_t czasMiedzyZadaniamiSignal = registerSignal("czasMiedzyZadaniami");
        simsignal_t wielkoscZadaniaSignal = registerSignal("wielkoscZadania");

        emit(czasMiedzyZadaniamiSignal, czasMiedzyZadaniami);
        emit(wielkoscZadaniaSignal, wielkoscZadania);

    }
    else
    {
        delete msg;
    }
}

