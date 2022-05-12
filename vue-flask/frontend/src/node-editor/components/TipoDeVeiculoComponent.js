import Rete from "rete";
import * as Socket from "../sockets";

import { VehicleTypeControl } from "@/node-editor/controls/VehicleTypeControl/VehicleTypeControl";
import { NumControl } from '@/node-editor/controls/NumControl/NumControl'

export class TipoDeVeiculoComponent extends Rete.Component {
    constructor(){
        super("Tipo de Veículo");
    }

    builder(node) {
        var out1 = new Rete.Output('num', "Out", Socket.vehicle);
        return node
          .addControl(new VehicleTypeControl(this.editor, 'Road'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}