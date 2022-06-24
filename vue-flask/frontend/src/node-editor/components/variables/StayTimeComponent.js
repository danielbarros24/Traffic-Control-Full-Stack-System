import Rete from "rete";
import * as Socket from "../../sockets";

import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/variables/Node.vue";

export class StayTimeComponent extends Rete.Component {
    constructor(){
        super("Stay Time");
        this.data.component = Node;
    }

    async builder(node) {

        const urlDesktop = "127.0.0.1:5000"
        const urlRasp = "192.168.1.216:5000"
        
        const responseZones = await fetch(`http://${urlRasp}/sensors`, {headers: {
            'Authorization': `Bearer ${localStorage.getItem("token")}`
          }});
        const sensors = await responseZones.json();

        let all = []


        for (let x in sensors) {

            let sensor = sensors[x]
            let lanes = sensor.lanes

            let n = 1

            let aux = []

            while (lanes > 0) {

                aux = [];
                aux.push(sensor.name);
                aux.push(n);

                all.push(aux);

                n ++;
                lanes --;

            }
        } 

        var out = new Rete.Output('num', "Out", Socket.number);

        return node
            .addControl(new SelectControl(this.editor, 'vehicle', [
                { text: 'All', value: 'ALL' },
                { text: 'Car', value: 'CAR' },
                { text: 'Truck', value: 'TRUCK' },
                { text: 'Bike', value: 'BIKE' }
            ], "Vehicle Type"))
            .addControl(new SelectControl(this.editor, 'zone', all.map((value) => ({
                text: `${value[0]} - Lane ${value[1]}`, value: `${value[0]}-${value[1]}`,
            })), "Zone"))
            .addOutput(out);
    }

    worker(node, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const vehicleType = node.data.vehicle;
        const zone = node.data.zone;

        return {
            "stayTime": [ zone, vehicleType ]
        }  
    }
}