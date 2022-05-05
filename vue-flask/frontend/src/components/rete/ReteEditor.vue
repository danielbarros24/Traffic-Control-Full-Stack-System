<template>
  <div>
    <div class="wrapper"><div class="node-editor" ref="nodeEditor"></div></div>
    <canvas id="canvasOutput"></canvas>
  </div>
</template>

<script>
import { Socket, NodeEditor, Control, Output, Input, Component, Engine } from "rete";

import ConnectionPlugin from "rete-connection-plugin";
import VueRenderPlugin from "rete-vue-render-plugin";
import ContextMenuPlugin from "rete-context-menu-plugin";
import AreaPlugin from "rete-area-plugin";
import KeyboardPlugin from 'rete-keyboard-plugin';

import ReteNumControl from './ReteNumControl'

export default {
  data() {
    return {
      editor: null
    };
  },

  async mounted() {
    var numSocket = new Socket('Number value');

    class NumControl extends Control {
      constructor(emitter, key, readonly) {
        super(key);
        
        this.component = ReteNumControl;
        this.props = { emitter, ikey: key, readonly };
      }

      setValue(val) {
        this.vueContext.value = val;
      }
    }

    class ConstantComponent extends Component {
        constructor(){
            super("Constant");
        }

        builder(node) {
            var out1 = new Output('num', "Number", numSocket);
            return node
              .addControl(new NumControl(this.editor, 'num'))
              .addOutput(out1);
        }

        worker(node, inputs, outputs) {
            outputs['num'] = node.data.num;
        }
    }

    class AddComponent extends Component {
        constructor(){
            super("Add");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addControl(new NumControl(this.editor, 'preview', true))
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) => partialSum + a, 0);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class MultiplyComponent extends Component {
        constructor(){
            super("Multiply");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addControl(new NumControl(this.editor, 'preview', true))
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum * a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class DivisionComponent extends Component {
        constructor(){
            super("Divide");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addControl(new NumControl(this.editor, 'preview', true))
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    class EqualToComponent extends Component {
        constructor(){
            super("=");
        }
        
        builder(node) {
            var inp1 = new Input('num',"Number", numSocket, true);
            var out = new Output('num', "Number", numSocket);

            return node
                .addInput(inp1)
                .addOutput(out);
        }
        
        worker(node, inputs, outputs) {
            var sum = inputs['num'].reduce((partialSum, a) =>  partialSum / a, 1);
            this.editor.nodes.find(n => n.id == node.id).controls.get('preview').setValue(sum);
            outputs['num'] = sum;
        }
    }

    var container = this.$refs.nodeEditor
    var components = [new ConstantComponent(), new AddComponent(), new MultiplyComponent(), new DivisionComponent(), new EqualToComponent()];
    var editor = new NodeEditor('demo@0.1.0', container);

    editor.use(ConnectionPlugin);
    editor.use(VueRenderPlugin);
    editor.use(ContextMenuPlugin);
    editor.use(AreaPlugin);
    editor.use(KeyboardPlugin);

    var engine = new Engine('demo@0.1.0');
    components.map(c => {
        editor.register(c);
        engine.register(c);
    });

    var n1 = await components[0].createNode({num: 2});
    var n2 = await components[0].createNode({num: 0});
    var add = await components[1].createNode();
    var sub = await components[2].createNode();
    

    n1.position = [80, 200];
    n2.position = [80, 400];
    add.position = [500, 240];
    sub.position = [800, 240];

    editor.addNode(n1);
    editor.addNode(n2);
    editor.addNode(add);
    editor.addNode(sub);

    editor.connect(n1.outputs.get('num'), add.inputs.get('num'));
    editor.connect(n2.outputs.get('num'), add.inputs.get('num2'));
    editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async () => {
      console.log('process');
        await engine.abort();
        await engine.process(editor.toJSON());
        console.log(editor.toJSON())
    });
    
    editor.view.resize();
    AreaPlugin.zoomAt(editor);
    editor.trigger('process');
  }
};
</script>

<style>
.node-editor {
  text-align: left;
  height: 100vh;
  width: 100vw;
}
.node .control input, .node .input-control input {
  width: 140px;
}
select, input {
  width: 100%;
  border-radius: 30px;
  background-color: white;
  padding: 2px 6px;
  border: 1px solid #999;
  font-size: 110%;
  width: 170px;
}
</style>