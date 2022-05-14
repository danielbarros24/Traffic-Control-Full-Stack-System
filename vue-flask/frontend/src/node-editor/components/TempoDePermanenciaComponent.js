import Rete from "rete";
import * as Socket from "../sockets";

import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";
import { ZoneControl } from "@/node-editor/controls/ZoneControl/ZoneControl"

export class TempoDePermanenciaComponent extends Rete.Component {
    constructor(){
        super("Tempo de permanência");
    }

    builder(node) {
        var out = new Rete.Output('num', "Out", Socket.number);

        return node
            .addControl(new SelectControl(this.editor, 'type', [
                { text: 'All', value: 'ALL' },
                { text: 'Car', value: 'CAR' },
                { text: 'Truck', value: 'TRUCK' },
                { text: 'Motocycle', value: 'MOTO' }
            ], "Vehicle Type"))
            .addControl(new ZoneControl(this.editor, 'zone'))
            .addOutput(out);
    }

    worker(node, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const type = node.data.type;
        const zone = node.data.zone;


        /*
        {
            "stayTime": [ TYPE, ZONE ]
        }
        */


        return {
            "stayTime": [ type, zone ]
        }  
    }
}