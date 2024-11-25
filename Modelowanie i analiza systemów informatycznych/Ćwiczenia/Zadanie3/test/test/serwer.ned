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

module Serwer
{
    parameters:
        
        @display("bgb=260,127;i=device/server2");
    gates:
        inout odDoPrzelacznika;
        
    submodules:
        cpu: Procesor {
            jednostkowyCzasObslugi = default(1.0);
            @display("p=39,42");
        }
        hdd: Dysk {
            jednostkowyCzasObslugi = default(1.0);
            @display("p=127,44");
        }
    connections:
        odDoPrzelacznika <--> cpu.odDoSerwera;
        hdd.doOdProcesora <--> cpu.doOdDysku;

}
