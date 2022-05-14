import Rete from "rete";
import * as Socket from "../sockets";

import { SelectControl } from "@/node-editor/controls/SelectControl/SelectControl";
import { NumControl } from '@/node-editor/controls/NumControl/NumControl'

export class TipoDeVeiculoComponent extends Rete.Component {
    constructor(){
        super("Tipo de Veículo");
    }

    builder(node) {
        var out1 = new Rete.Output('num', "Out", Socket.vehicle);

        return node
          .addControl(new SelectControl(this.editor, 'type', [
            { text: 'All', value: 'ALL' },
            { text: 'Car', value: 'CAR' },
            { text: 'Truck', value: 'TRUCK' },
            { text: 'Motocycle', value: 'MOTO' }
          ], "Vehicle Type"))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.type;
    }

    toJsonLogic(node) {
        return node.data.type;
    }
}