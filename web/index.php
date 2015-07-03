<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>Command Line</title>
    <script type="application/javascript" src="fast-click/lib/fastclick.js"></script>
</head>
<body>

<!--Open	Close	Read 	Write	Schedule	Server	Start-->
<!--Patch	One2One	Define	As	All	ID	Stop-->
<!--Fixture	Channel	DMX	{	}	;	,-->
<!--Load	Unload	Pause	Unpause	Full	Insert	-->
<!--Save	%	Thru	At	Except	Cued	-->
<!--Group	7	8	9	And	Step	-->
<!--Sequence	4	5	6	Enter	Wait	List-->
<!--Scene	1	2	3		Fade	Print-->

<div id="container">
    <table>
        <tr>
            <td colspan="7" style="height: 20%">
                <div id="log"></div>
                <input type="text" id="command_input" onkeydown="onKeypress(event)"/>
            </td>
        </tr>
        <tr>
            <td><button class="util" ontouchstart="addToCommand(' open ', false)" onmousedown="addToCommand(' open ', false)">Open</button></td>
            <td><button class="util" ontouchstart="addToCommand(' close ', false)" onmousedown="addToCommand(' close ', false)">Close</button></td>
            <td><button class="util" ontouchstart="addToCommand(' read ', false)" onmousedown="addToCommand(' read ', false)">Read</button></td>
            <td><button class="util" ontouchstart="addToCommand(' write ', false)" onmousedown="addToCommand(' write ', false)">Write</button></td>
            <td><button class="util" ontouchstart="addToCommand(' schedule ', false)" onmousedown="addToCommand(' schedule ', false)">Schedule</button></td>
            <td><button class="util" ontouchstart="promtConnection()"  onmousedown="promtConnection()">Change Server</button></td>
            <td><button class="util" ontouchstart="connect()"          onmousedown="connect()">Connect</button></td>
        </tr>
        <tr>
            <td><button class="util" ontouchstart="addToCommand(' patch ', false)"      onmousedown="addToCommand(' patch ', false)">Patch</button></td>
            <td><button class="util" ontouchstart="addToCommand(' one-to-one ', false)" onmousedown="addToCommand(' one-to-one ', false)">One-to-One</button></td>
            <td><button class="util" ontouchstart="addToCommand(' define ', false)"     onmousedown="addToCommand(' define ', false)">Define</button></td>
            <td><button class="util" ontouchstart="addToCommand(' as  ', false)"        onmousedown="addToCommand(' as  ', false)">As</button></td>
            <td><button class="util" ontouchstart="addToCommand(' all ', false)"        onmousedown="addToCommand(' all ', false)">All</button></td>
            <td><button class="util" ontouchstart="addToCommand(' id ', false)"         onmousedown="addToCommand(' id ', false)">ID</button></td>
            <td><button class="enter" ontouchstart="addToCommand(' bo ', false)"         onmousedown="addToCommand(' bo ', false)">Blackout</button></td>
        </tr>
        <tr>
            <td><button class="type" onclick="addToCommand(' fixture ', true)">Fixture</button></td>
            <td><button class="type" ontouchstart="addToCommand(' channel ', false)" onmousedown="addToCommand(' channel ', false)">Channel</button></td>
            <td><button class=x"type" ontouchstart="addToCommand(' dmx ', false)" onmousedown="addToCommand(' dmx ', false)">DMX</button></td>
            <td><button class="symbols" ontouchstart="addToCommand(' { ', false)" onmousedown="addToCommand(' { ', false)">{</button></td>
            <td><button class="symbols" ontouchstart="addToCommand(' } ', false)" onmousedown="addToCommand(' } ', false)">}</button></td>
            <td><button class="symbols" ontouchstart="addToCommand(';', false)" onmousedown="addToCommand(';', false)">;</button></td>
            <td><button class="symbols" ontouchstart="addToCommand(' ,', false)" onmousedown="addToCommand(' ,', false)">,</button></td>
        </tr>
        <tr>
            <td><button class="sequence-running" ontouchstart="addToCommand(' load ', false)" onmousedown="addToCommand(' load ', false)">Load</button></td>
            <td><button class="sequence-running" ontouchstart="addToCommand(' unload ', false)" onmousedown="addToCommand(' unload ', false)">Unload</button></td>
            <td><button class="sequence-running" ontouchstart="addToCommand(' pause ', false)" onmousedown="addToCommand(' pause ', false)">Pause</button></td>
            <td><button class="sequence-running" ontouchstart="addToCommand(' unpause ', false)" onmousedown="addToCommand(' unpause ', false)">Unpause</button></td>
            <td><button class="sequence-running" ontouchstart="addToCommand(' advance ', false)" onmousedown="addToCommand(' advance ', false)">Advance</button></td>
            <td><button class="symbols" ontouchstart="addToCommand('&quot;', false)" onmousedown="addToCommand('&quot;', false)">&quot;</button></td>
            <td><button class="symbols" ontouchstart="addToCommand(':', false)" onmousedown="addToCommand(':', false)">:</button></td>
        </tr>
        <tr>
            <td><button class="save" ontouchstart="addToCommand(' save ', false)" onmousedown="addToCommand(' save ', false)">Save</button></td>
            <td><button class="basic-control" ontouchstart="addToCommand('%', false)" onmousedown="addToCommand('%', false)">%</button></td>
            <td><button class="basic-control" ontouchstart="addToCommand(' thru ', false)" onmousedown="addToCommand(' thru ', false)">Thru</button></td>
            <td><button class="basic-control" ontouchstart="addToCommand(' at ', false)" onmousedown="addToCommand(' at ', false)">At</button></td>
            <td><button class="basic-control" ontouchstart="addToCommand(' except ', false)" onmousedown="addToCommand(' except ', false)">Except</button></td>
            <td><button class="printing" ontouchstart="backspace_command()" onmousedown="backspace_command()">Backspace</button></td>
            <td><button class="sequence-options" ontouchstart="addToCommand(' insert ', false)" onmousedown="addToCommand(' insert ', false)">Insert</button></td>
        </tr>
        <tr>
            <td><button class="util" onclick="addToCommand(' group ', true)">Group</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('7', false)" onmousedown="addToCommand('7', false)">7</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('8', false)" onmousedown="addToCommand('8', false)">8</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('9', false)" onmousedown="addToCommand('9', false)">9</button></td>
            <td><button class="basic-control" ontouchstart="addToCommand(' and ', false)" onmousedown="addToCommand(' and ', false)">And</button></td>
            <td><button class="basic-control" ontouchstart="addToCommand(' 100 ', false)" onmousedown="addToCommand(' 100 ', false)">Full</button></td>
            <td><button class="sequence-options" ontouchstart="addToCommand(' cued ', false)" onmousedown="addToCommand(' cued ', false)">Cued</button></td>
        </tr>
        <tr>
            <td><button class="util" onclick="addToCommand(' sequence ', true)">Sequence</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('4', false)" onmousedown="addToCommand('4', false)">4</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('5', false)" onmousedown="addToCommand('5', false)">5</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('6', false)" onmousedown="addToCommand('6', false)">6</button></td>
            <td rowspan="3"><button class="enter" ontouchstart="runCommand()" onmousedown="runCommand()">Enter</button></td>
            <td><button class="printing" ontouchstart="clear_command()" onmousedown="clear_command()">Clear</button></td>
            <td><button class="sequence-options" ontouchstart="addToCommand(' step ', false)" onmousedown="addToCommand(' step ', false)">Step</button></td>
        </tr>
        <tr>
            <td><button class="util" onclick="addToCommand('scene ', true)">Scene</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('1', false)" onmousedown="addToCommand('1', false)">1</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('2', false)" onmousedown="addToCommand('2', false)">2</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('3', false)" onmousedown="addToCommand('3', false)">3</button></td>
            <td><button class="printing" ontouchstart="addToCommand('list ', false)" onmousedown="addToCommand('list ', false)">List</button></td>
            <td><button class="sequence-options" ontouchstart="addToCommand(' wait ', false)" onmousedown="addToCommand(' wait ', false)">Wait</button></td>
        </tr>
        <tr>
            <td><button class="save" ontouchstart="addToCommand(' delete ', false)" onmousedown="addToCommand(' delete ', false)">Delete</button></td>
            <td colspan="2"><button class="numbers" ontouchstart="addToCommand('0', false)" onmousedown="addToCommand('0', false)">0</button></td>
            <td><button class="numbers" ontouchstart="addToCommand('.', false)" onmousedown="addToCommand('.', false)">.</button></td>
            <td><button class="printing" ontouchstart="addToCommand(' print ', false)" onmousedown="addToCommand(' print ', false)">Print</button></td>
            <td><button class="sequence-options" ontouchstart="addToCommand(' fade ', false)" onmousedown="addToCommand(' fade ', false)">Fade</button></td>
        </tr>
    </table>
</div>
</body>
<style>
    body{
        width: 100%;
    }

    #container
    {
        height: 100%;
        min-height: 100%;
    }
    table
    {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        height:100%;
        table-layout: fixed;
    }
    tr
    {
        border: solid black 1px;
        table-layout: fixed;
        height: 9%;
    }
    td
    {
        /*border: solid black 1px;*/
        table-layout: fixed;
        width: 14.3%;
        padding: 2px;
    }

    button
    {
        width: 100%;
        height: 100%;
        font-size: 15px;
        -webkit-appearance: none;
    }

    button:active
    {
        background-color: #FFFFFF;
    }

    input
    {
        height: 20%;
        font-size: 100%;
    }

    #command_input
    {
        width: 98%;
    }

    #log
    {
        width: 100%;
        height: 85%;
        overflow: scroll;
    }

    /* Color Styles */
    .util
    {
        background-color: #F1F1F1;
    }
    .type
    {
        background-color: #c0d2f5;
    }
    .symbols
    {
        background-color: #f0c2c3;
    }
    .sequence-running
    {
        background-color: #fdf0c3;
    }
    .sequence-options
    {
        background-color: #d1c8e3;
    }
    .save
    {
        background-color: #c7dadc;
    }
    .basic-control
    {
        background-color: #e4c7d5;
    }
    .printing
    {
        background-color: #f9dfc4;
    }
    .save-types
    {
        background-color: #d2e6ca;
    }
    .numbers
    {
        background-color: #c6dcf0;
    }
    .enter
    {
        background-color: #0b0b0b;
        color: #FFFFFF;
    }

</style>

<script>
        if ('addEventListener' in document) {
            document.addEventListener('DOMContentLoaded', function () {
                FastClick.attach(document.body);
            }, false);
        }


        function onKeypress(event) {
            if (event.keyCode == 13) // On enter press
            {
                runCommand();
                return false; // returning false will prevent the event from bubbling up.
            }
            return true;
        }

        function print(str)
        {
            element = document.getElementById("log");
            current = element.innerHTML;
            element.innerHTML = current + str + "<br />" ;
            element.scrollTop = element.scrollHeight;
        }

        var name = "<?php print $_SERVER['SERVER_ADDR']; ?>";
        var socket = null;
        function promtConnection()
        {
            name = prompt("Please enter the server address: ", name);
            connect()
        }

        function connect() {
            if (socket != null)
            {
                socket.close();
            }
            var address = "ws://" + name + ":8080/ws";
            print("Attempting to connect at " + address);
            socket = new WebSocket(address);

            socket.onerror = function(event){
                print("Connection error; could not connect to socket");
            };

            socket.onopen = function(event){
                print("Connected to server at " + socket.url);
            };

            socket.onclose = function(event){
                print("Could not connect to server");
            };

            socket.onmessage = function (event)
            {
                print(event.data);
            };

        }

        function send_message(command)
        {
            try {
                socket.send(command);
            }
            catch(e)
            {
                if (e.message == "socket is not defined") {
                    print("Connection has not been made yet. Connect to the server")
                }
            }
        }

        function runCommand() {
            element = document.getElementById("command_input");
            command = element.value;

            print(">>> " + command);
            send_message(command);
            clear_command();
        }

        function clear_command()
        {
            element = document.getElementById("command_input");
            element.value = ""
        }

        function backspace_command()
        {
            element = document.getElementById("command_input");
            element.value = element.value.substr(0, element.value.length - 1);
        }

        function addToCommand(str, focus) {
            element = document.getElementById("command_input");
            current = element.value;
            element.value = current + str;
            if (focus) {
                element.focus();
            }
        }

</script>
</html>






















