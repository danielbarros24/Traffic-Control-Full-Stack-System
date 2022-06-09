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

        const responseZones = await fetch("http://127.0.0.1:5000/settings-zones");
        const zones = await responseZones.json();

        
        const all = []

        for (const x in zones.Zones) {
            const sensor = zones.Zones[x].split('-')
            const sensorNumber = sensor[0].replace( /[^\d.]/g, '' )

            const aux = []
            aux.push(sensorNumber)
            aux.push(sensor[1])

            all.push(aux)
        }

        var out = new Rete.Output('num', "Out", Socket.number);

        return node
            .addControl(new SelectControl(this.editor, 'type', [
                { text: 'All', value: 'ALL' },
                { text: 'Car', value: 'CAR' },
                { text: 'Truck', value: 'TRUCK' },
                { text: 'Bike', value: 'BIKE' }
            ], "Vehicle Type"))
            .addControl(new SelectControl(this.editor, 'type1', all.map((value) => ({
            text: `Sensor ${value[0]} - Lane ${value[1]}`, value: `T${value[0]}-${value[1]}`,
          })), "Zone"))
            .addOutput(out);
    }

    worker(node, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const vehicleType = node.data.type;
        const zone = node.data.type1;

        return {
            "stayTime": [ zone, vehicleType ]
        }  
    }
}