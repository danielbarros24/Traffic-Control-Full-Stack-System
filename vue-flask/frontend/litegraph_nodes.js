// HERE ALL NODES WILL BE CREATED
///////////////////////////////////

//-----------------------------------------OPERATIONS-------------------------------------------//
//--------------------SUM NODE------------------------//
//node constructor class
function sum(a,b)
{
   return a+b;
}

LiteGraph.wrapFunctionAsNode("math/sum",sum, ["Number","Number"],"Number");
//------------------------------------------------------------//


//--------------------SUBTRACTION NODE------------------------//
//node constructor class
function MyAddNode()
{
  this.addInput("A","number");
  this.addInput("B","number");
  this.addOutput("A+B","number");
  this.properties = { precision: 1 };
}

//name to show
MyAddNode.title = "Subtraction";

//function to call when the node is executed
MyAddNode.prototype.onExecute = function()
{
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  var B = this.getInputData(1);
  if( B === undefined )
    B = 0;
  this.setOutputData( 0, A - B );
}

//register in the system
LiteGraph.registerNodeType("basic/subtraction", MyAddNode );
//----------------------------------------------------------------//

//--------------------MULTIPLICATION NODE------------------------//
//node constructor class
function MyAddNode()
{
  this.addInput("A","number");
  this.addInput("B","number");
  this.addOutput("AxB","number");
  this.properties = { precision: 1 };
}

//name to show
MyAddNode.title = "Multiplication";

//function to call when the node is executed
MyAddNode.prototype.onExecute = function()
{
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  var B = this.getInputData(1);
  if( B === undefined )
    B = 0;
  this.setOutputData( 0, A * B );
}

//register in the system
LiteGraph.registerNodeType("basic/division", MyAddNode );
//--------------------------------------------------------//

//--------------------DIVISON NODE------------------------//
//node constructor class
function MyAddNode()
{
  this.addInput("A","number");
  this.addInput("B","number");
  this.addOutput("A/B","number");
  this.properties = { precision: 1 };
}

//name to show
MyAddNode.title = "Division";

//function to call when the node is executed
MyAddNode.prototype.onExecute = function()
{
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  var B = this.getInputData(1);
  if( B === undefined )
    B = 0;
  this.setOutputData( 0, A / B );
}

//register in the system
LiteGraph.registerNodeType("basic/division", MyAddNode );
//----------------------------------------------------//

//--------------------GREATER THAN NODE------------------------//
//node constructor class
function MyAddNode()
{
  this.addInput("In1","number");
  this.addInput("In2","number");
  this.addOutput("Out","number");
  this.properties = { precision: 1 };
}

//name to show
MyAddNode.title = "Greater Than";

//function to call when the node is executed
MyAddNode.prototype.onExecute = function()
{
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  var B = this.getInputData(1);
  if( B === undefined )
    B = 0;
  this.setOutputData( 0, A > B );
}

//register in the system
LiteGraph.registerNodeType("basic/greater_than", MyAddNode );
//----------------------------------------------------//

//--------------------LESS THAN NODE------------------------//
//node constructor class
function MyAddNode()
{
  this.addInput("In1","number");
  this.addInput("In2","number");
  this.addOutput("Out","number");
  this.properties = { precision: 1 };
}

//name to show
MyAddNode.title = "Less Than";

//function to call when the node is executed
MyAddNode.prototype.onExecute = function()
{
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  var B = this.getInputData(1);
  if( B === undefined )
    B = 0;
  this.setOutputData( 0, A < B );
}

//register in the system
LiteGraph.registerNodeType("basic/less_than", MyAddNode );
//----------------------------------------------------//

//--------------------EQUAL TO NODE------------------------//
//node constructor class
function MyAddNode()
{
  this.addInput("In1","number");
  this.addInput("In2","number");
  this.addOutput("Out","number");
  this.properties = { precision: 1 };
}

//name to show
MyAddNode.title = "Equal To";

//function to call when the node is executed
MyAddNode.prototype.onExecute = function()
{
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  var B = this.getInputData(1);
  if( B === undefined )
    B = 0;
  this.setOutputData( 0, A == B );
}

//register in the system
LiteGraph.registerNodeType("basic/equal_to", MyAddNode );
//----------------------------------------------------//
//----------------------------------------------------------------------------------------------//


//-----------------------------------------CONDITIONS-------------------------------------------//
//--------------------AND NODE------------------------//
//node constructor class
function MyAddNode()
{
  this.addInput("In1","number");
  this.addInput("In2","number");
  this.addOutput("Out","number");
  this.properties = { precision: 1 };
}

//name to show
MyAddNode.title = "AND";

//function to call when the node is executed
MyAddNode.prototype.onExecute = function()
{
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  var B = this.getInputData(1);
  if( B === undefined )
    B = 0;
  this.setOutputData( 0, A & B );
}

//register in the system
LiteGraph.registerNodeType("basic/and", MyAddNode );
//----------------------------------------------------//

//--------------------OR NODE------------------------//
//node constructor class
function MyAddNode()
{
  this.addInput("In1","number");
  this.addInput("In2","number");
  this.addOutput("Out","number");
  this.properties = { precision: 1 };
}

//name to show
MyAddNode.title = "OR";

//function to call when the node is executed
MyAddNode.prototype.onExecute = function()
{
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  var B = this.getInputData(1);
  if( B === undefined )
    B = 0;
  this.setOutputData( 0, A | B );
}

//register in the system
LiteGraph.registerNodeType("basic/or", MyAddNode );
//----------------------------------------------------//

//--------------------NOT NODE------------------------//
//node constructor class
function MyAddNode()
{
  this.addInput("In1","number");
  this.addOutput("Out","number");
  this.properties = { precision: 1 };
}

//name to show
MyAddNode.title = "NOT";

//function to call when the node is executed
MyAddNode.prototype.onExecute = function()
{
  var A = this.getInputData(0);
  if( A === undefined )
    A = 0;
  this.setOutputData( 0, !A );
}

//register in the system
LiteGraph.registerNodeType("basic/not", MyAddNode );
//----------------------------------------------------//
//---------------------------------------------------------------------------------------------//