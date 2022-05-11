import Rete from "rete";
import * as Socket from "../sockets";

import { NumControl } from '@/node-editor/controls/NumControl/NumControl'

export class TipoDeVeiculoComponent extends Rete.Component {
    constructor(){
        super("Tipo de Veículo");
    }

    builder(node) {
        var out1 = new Rete.Output('str', "Out", Socket.vehicle);
        return node
          .addControl(new NumControl(this.editor, 'Road'))
          .addOutput(out1);
    }

    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}