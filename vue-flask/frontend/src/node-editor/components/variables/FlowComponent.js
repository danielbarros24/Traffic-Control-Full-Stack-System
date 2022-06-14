import Rete from "rete";
import * as Socket from "../../sockets";

import { TimeControl } from "@/node-editor/controls/TimeControl/TimeControl";
import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/variables/Node.vue";

export class FlowComponent extends Rete.Component {
    constructor(){
        super("Flow");
        this.data.component = Node;
    }

    async builder(node) {

        const urlDesktop = "127.0.0.1:5000"
        const urlRasp = "192.168.1.216:8080"
        const responseZones = await fetch(`http://${urlDesktop}/sensors`);
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
        var out1 = new Rete.Output('num', "Out", Socket.number);

        return node
    
          .addControl(new SelectControl(this.editor, 'type', [
            { text: 'All', value: 'ALL' },
            { text: 'Car', value: 'CAR' },
            { text: 'Truck', value: 'TRUCK' },
            { text: 'Bike', value: 'BIKE' }
          ], "Vehicle Type"))
          .addControl(new SelectControl(this.editor, 'type1', all.map((value) => ({
            text: `${value[0]} - Lane ${value[1]}`, value: `${value[0]}-${value[1]}`,
        })), "Zone"))
          .addControl(new TimeControl(this.editor, 'str'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
    toJsonLogic(node) {
        const zone = node.data.type1;
        const vehicleType = node.data.type;
        const duration = node.data.str;

        return {
            "flow": [ zone, vehicleType, duration ]
        }  
    }
}