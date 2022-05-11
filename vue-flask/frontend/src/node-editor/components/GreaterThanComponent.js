import Rete from "rete";
import * as Socket from "../sockets";

export class GreaterThanComponent extends Rete.Component {
    constructor(){
        super(">");
    }
    
    builder(node) {
        var inp1 = new Rete.Input('num1',"In1", Socket.number);
        var inp2 = new Rete.Input('num2',"In2", Socket.number);
        var out = new Rete.Output('num', "Out", Socket.number);

        return node
            .addInput(inp1)
            .addInput(inp2)
            .addOutput(out);
    }
    
    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }
}