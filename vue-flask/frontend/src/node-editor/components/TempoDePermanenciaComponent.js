import Rete from "rete";
import * as Socket from "../sockets";

import { VehicleTypeControl } from "@/node-editor/controls/VehicleTypeControl/VehicleTypeControl";
import { ZoneControl } from "@/node-editor/controls/ZoneControl/ZoneControl"

export class TempoDePermanenciaComponent extends Rete.Component {
    constructor(){
        super("Tempo de permanência");
    }

    builder(node) {
        var out = new Rete.Output('num', "Out", Socket.number);

        return node

            .addControl(new VehicleTypeControl(this.editor, 'str'))
            .addControl(new ZoneControl(this.editor, 'str1'))
            .addOutput(out);
    }

    worker(node, outputs) {
        outputs['num'] = node.data.num;
    }
}