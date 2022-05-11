import Rete from "rete";
import * as Socket from "../sockets";

export class ANDComponent extends Rete.Component {
    constructor(){
        super("AND");
    }
    
    builder(node) {
        var inp1 = new Rete.Input('num',"In", Socket.number, true);
        var out = new Rete.Output('num', "Out", Socket.number);

        return node
            .addInput(inp1)
            .addOutput(out);
    }
    
    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}