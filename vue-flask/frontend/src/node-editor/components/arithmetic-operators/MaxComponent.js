import Rete from "rete";
import * as Socket from "../../sockets";
import Node from "../../../../node_modules/rete-vue-render-plugin/src/arithmetic-operators/Node.vue";

export class MaxComponent extends Rete.Component {
    constructor(){
        super("Max");
        this.data.component = Node;
    }
    
    builder(node) {
        var inp1 = new Rete.Input('num1',"In", Socket.number, true);
        var out = new Rete.Output('num', "Out", Socket.number);

        return node
            .addInput(inp1)
            .addOutput(out);
    }
    
    worker(node, inputs, outputs) {
        outputs['num'] = node.data.num;
    }

    toJsonLogic(node) {
        const { inputs } = node;
        
        const inputNum = inputs.get('num1');
        const { connections } = inputNum;

        return {
            "max": connections.map(connection => {
                const connectionNode = connection.output.node;
                const connectionComponent = this.editor.getComponent(connectionNode.name);
                return connectionComponent.toJsonLogic?.(connectionNode)
            })  
        }  
    }
}