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

network Symulator
{
    parameters:
        @display("bgb=500,500");
        int liczbaKlientow;
    submodules:
        klient[liczbaKlientow]: Klient {
            idKlienta = index;
            @display("p=50,50+50*index");
        }
        przelacznik: Przelacznik {
            liczbaBramKlient = parent.liczbaKlientow;
            @display("p=200,150");
        }
        serwer: Serwer {
            @display("p=400,150");
        }
    connections:
        for i=0..liczbaKlientow-1 {
            klient[i].odDoPrzelacznika <--> przelacznik.odDoKlienta[i];
        }

        przelacznik.odDoSerwera <--> serwer.odDoPrzelacznika;
}
