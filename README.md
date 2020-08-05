<h1 id="huskylens-python-api">HUSKYLENS Python API</h1>
<pre><code>Author   : Robert (robert@dfrobot.com) 
Version  : 0.1
Date     : 08/04/2020
Github   : <a href="/huskylib.py">Github</a>
</code></pre>
<hr>
<h3 id="quick-start">Quick Start</h3>
<blockquote>
<p>USB Connection (Mac/Windows/Linux -&gt; Huskylens)</p>
<ul>
<li><code>pip3 install pyserial pypng</code></li>
<li>Place the <a href="/huskylib.py">huskylib.py</a> file within your projects folder</li>
<li><code>from huskylib import HuskyLensLibrary</code></li>
<li><code>hl = HuskyLensLibrary("SERIAL", "/dev/ttyUSB0")</code></li>
<li><code>print(h1.knock()</code></li>
</ul>
<p>Raspberry Pi (I2C -&gt; Huskylens)</p>
<ul>
<li>Please refer to our full guide <a href="/Raspberry Pi Tutorial.md"> here:</a></li>
</ul>
</blockquote>

### Example Script
> You can test out all the functions in our provided example script. Simply run `exampleHL.py` after changing the the connection settings in the beginning of the file. You will need a terminal / IDE to interact with the script. 

<h4 id="guide-format-information">Function Format Information</h4>
<blockquote>
<dl>
<dt>function_name(ARG1,ARG2,…)</dt>
<dd>
<dl>
<dt>Description:</dt>
<dd>Short description of functions overall inputs and its corresponding functionality</dd>
</dl>
</dd>
<dd>
<dl>
<dt>Arguments:</dt>
<dd>Arg1 : (Variable Type) Description</dd>
<dd>Arg2 : (Variable Type) Description</dd>
</dl>
</dd>
<dd>
<dl>
<dt>Returns:</dt>
<dd>Short description the return value of the function, NONE if the function does not return</dd>
</dl>
</dd>
</dl>
</blockquote>
<br>
<h2 id="general-functions">General Functions</h2>
<dl>
<dt>HuskyLensLibrary(“COM_PROTOCOL”, “COM_PORT”,  channel,  address)</dt>
<dd>
<p><strong>Description:</strong> Instantiate the HuskyLens class and automatically connect to your HuskyLens. This return the main object that you will run all functions  on.</p>
</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd><code>"COM_PROTOCOL"</code> : (String) Either <code>"SERIAL"</code> for USB connections or <code>"I2C"</code> for Raspberry Pi I2C.</dd>
<dd><code>"COM_PORT"</code> : (String) COM Port of the HuskyLens. Not needed for <code>"I2C"</code> connections.</dd>
<dd><code>"i2c_channel"</code> : (Integer) I2C Channel, refer to Raspberry Pi Guide. Not needed for <code>"SERIAL"</code>.</dd>
<dd><code>"i2c_channel"</code> : (Integer) I2C Channel, refer to Raspberry Pi Guide. Not needed for <code>"SERIAL"</code>.</dd>
</dl>
</dd>
<dd>
<p><strong>Returns:</strong> Returns <code>HuskyLens</code> object</p>
</dd>
<dd>
<dl>
<dt><strong>Examples:</strong></dt>
<dd><code>hl = HuskyLensLibrary("SERIAL", "/dev/ttyUSB0")</code></dd>
<dd><code>hl = HuskyLensLibrary("I2C","", address=0x32, channel=0)</code><br>
<br></dd>
</dl>
</dd>
<dt>knock()</dt>
<dd>
<p><strong>Description:</strong> Send a simple <em>knock</em> to the HuskyLens to ensure that you are connected and can communicate.</p>
</dd>
<dd>
<p><strong>Returns:</strong> Returns “Knock Received” on success<br>
<br></p>
</dd>
<dt>frameNumber( )</dt>
<dd>
<p><strong>Description:</strong> Get the number of frame HUSKYLENS have processed.</p>
</dd>
<dd>
<p><strong>Returns:</strong> Frame Count</p>
</dd>
</dl>
<br>
<dl>
<dt>count( )</dt>
<dd>
<p><strong>Description:</strong> Get the number of learned and unlearned objects on the screen.</p>
</dd>
<dd>
<p><strong>Returns:</strong> Number of Ojbects on the Screen</p>
</dd>
</dl>
<br>
<dl>
<dt>learnedObjCount( )</dt>
<dd>
<p><strong>Description:</strong> Get the total number of learned objects for the current running algorithm, objects do not need to be present on screen.</p>
</dd>
<dd>
<p><strong>Returns:</strong> Number of learned objects</p>
</dd>
</dl>
<h2 id="data-functions">Data Functions</h2>
<blockquote>
<p><strong>Data Format</strong></p>
<ul>
<li>
<p>Data corresponds to either <code>block</code> information for all algorithms except <em>Line Tracking</em>, which instead will return <code>arrow</code> information. These directly reflect the blocks/arrows you see on the HusyLens UI.</p>
<pre><code>   class  Block:
   	Members:
   		x =&gt; (Integer) x coordinate of the center of the square 
   		y =&gt; (Integer) y coordinate of the center of the square 
   		width  =&gt;  (Integer) width of the square
   		height =&gt;  (Integer) height of the square
   		ID =&gt; (Integer) Objects ID (if not learned, ID is 0)
   		learned =&gt; (Boolean) True  if the object is learned
   		type =&gt; "BLOCK"
   class  Arrow:
   	Members:
   		xTail =&gt; (Integer) x coordinate of the tail of the arrow
   		yTail =&gt; (Integer) y coordinate of the tail of the arrow
   		xHead =&gt; (Integer) x coordinate of the head of the arrow
   		yHead =&gt; (Integer) y coordinate of the head of the arrow
   		ID =&gt; (Integer) Objects ID (if not learned, ID is 0)
   		learned =&gt; (Boolean) True  if the object is learned
   		type =&gt; "ARROW"
</code></pre>
</li>
<li>
<p>Returned data will be an array of either block or arrow information.:<br>
** <code>[block1 , block2, ... blockN]</code> or <code>[arrow1 , arrow2, ... arrowN]</code></p>
</li>
</ul>
</blockquote>
<br>
<dl>
<dt>requestAll( )</dt>
<dd><strong>Description:</strong> Request all block or arrow data from HuskyLens. This will return block/arrow data for all learned and unlearned objects that are visible on the screen.</dd>
<dd><strong>Returns:</strong>  Returns data array <code>[block1 , block2, ... blockN]</code> or <code>[arrow1 , arrow2, ... arrowN]</code><br>
<br></dd>
<dt>blocks()</dt>
<dd><strong>Description:</strong> Request all block data from HuskyLens. This will return block data for all learned and unlearned objects that are visible on the screen.</dd>
<dd><strong>Returns:</strong>  Returns data array <code>[block1 , block2, ... blockN]</code><br>
<br></dd>
<dt>arrows()</dt>
<dd><strong>Description:</strong> Request all arrow data from HuskyLens. This will return block data for all learned and unlearned objects that are visible on the screen.
<ul>
<li>Note this should be used on the <em>Line Tracking</em> algorithm</li>
</ul>
</dd>
<dd><strong>Returns:</strong>  Returns data array <code>[arrow1 , arrow2, ... arrowN]</code><br>
<br></dd>
<dt>learned( )</dt>
<dd><strong>Description:</strong> Request all block or arrow data from HuskyLens . This will return block/arrow data for all learned objects that are visible on the screen, unlearned objects are ignored.</dd>
<dd><strong>Returns:</strong>  Returns data array <code>[block1 , block2, ... blockN]</code> or <code>[arrow1 , arrow2, ... arrowN]</code><br>
<br></dd>
<dt>learnedBlocks( )</dt>
<dd><strong>Description:</strong> Request all block data from HuskyLens . This will return block data for all learned objects that are visible on the screen, unlearned objects are ignored.</dd>
<dd><strong>Returns:</strong>  Returns data array <code>[block1 , block2, ... blockN]</code><br>
<br></dd>
<dt>learnedArrows( )</dt>
<dd><strong>Description:</strong> Request all arrow data from HuskyLens . This will return arrow data for all learned objects that are visible on the screen, unlearned objects are ignored.
<ul>
<li>Note this should be used on the <em>Line Tracking</em> algorithm</li>
</ul>
</dd>
<dd><strong>Returns:</strong>  Returns data array <code>[arrow1 , arrow2, ... arrowN]</code><br>
<br></dd>
<dt>getObjectByID( ID )</dt>
<dd><strong>Description:</strong> Request all block or arrow data from HuskyLens that have a designated <strong>ID</strong> and are visible on screen.</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd><code>ID</code> : (Integer) The desired <code>ID</code> of the object</dd>
</dl>
</dd>
<dd><strong>Returns:</strong>  Returns data array <code>[block1 , block2, ... blockN]</code> or <code>[arrow1 , arrow2, ... arrowN]</code><br>
<br></dd>
<dt>getBlocksByID( ID )</dt>
<dd><strong>Description:</strong> Request all block data from HuskyLens that have a designated <strong>ID</strong> and are visible on screen.</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd><code>ID</code> : (Integer) The desired <code>ID</code> of the object</dd>
</dl>
</dd>
<dd><strong>Returns:</strong>  Returns data array <code>[block1 , block2, ... blockN]</code><br>
<br></dd>
<dt>getArrowsByID( ID )</dt>
<dd><strong>Description:</strong> Request all arrow data from HuskyLens that have a designated <strong>ID</strong> and are visible on screen.
<ul>
<li>Note this should be used on the <em>Line Tracking</em> algorithm</li>
</ul>
</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd><code>ID</code> : (Integer) The desired <code>ID</code> of the object</dd>
</dl>
</dd>
<dd><strong>Returns:</strong>  Returns data array <code>[arrow1 , arrow2, ... arrowN]</code><br>
<br></dd>
</dl>
<h2 id="algorithm-control-functions">Algorithm Control Functions</h2>
<dl>
<dt>algorthim( algorithmName)</dt>
<dd>
<p><strong>Description:</strong> Switch the HuskyLens to a specific algorithm.</p>
</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd>
<dl>
<dt><code>algorithmName</code> : (String) The desired algorithm to switch to.</dt>
<dd>
<blockquote>
<p>“ALGORITHM_OBJECT_TRACKING”<br>
“ALGORITHM_FACE_RECOGNITION”<br>
“ALGORITHM_OBJECT_RECOGNITION”<br>
“ALGORITHM_LINE_TRACKING”<br>
“ALGORITHM_COLOR_RECOGNITION”<br>
“ALGORITHM_TAG_RECOGNITION”<br>
“ALGORITHM_OBJECT_CLASSIFICATION”</p>
</blockquote>
</dd>
</dl>
</dd>
</dl>
</dd>
<dd>
<p><strong>Returns:</strong>  Returns “Knock Received” on success.<br>
<br></p>
</dd>
<dt>learn( ID )</dt>
<dd>
<p><strong>Description:</strong> Learn the current recognized object on screen with a chosen <strong>ID</strong></p>
</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd><code>ID</code> : (Integer) The desired <code>ID</code> of the object (1-1023 range)</dd>
</dl>
</dd>
<dd>
<p><strong>Returns:</strong>  Returns “Knock Received” on success.<br>
<br></p>
</dd>
<dt>forget( )</dt>
<dd>
<p><strong>Description:</strong> Forget learned objects for the current running algorithm.</p>
</dd>
<dd>
<p><strong>Returns:</strong>  Returns “Knock Received” on success.<br>
<br></p>
</dd>
</dl>
<h2 id="ui-related-functions">UI Related Functions</h2>
<dl>
<dt>setCustomName(“Name_Value”, objectID)</dt>
<dd><strong>Description:</strong> Set a custom name for a learned object with a specified ID. For example, if you have learned your face with an ID of 1, you can use huskylens.setCustomName(“Robert”,1) to rename the learned face to “Robert”.</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd><code>"Name_Value"</code> :  (String) value for the desired name</dd>
<dd><code>objectID</code> :     (Interger) value for the learned object ID you wish to change</dd>
</dl>
</dd>
<dd><strong>Returns:</strong>  Returns “Knock Received” on success<br>
<br></dd>
<dt>customText(“Text_Value”,  X, Y)</dt>
<dd><strong>Description:</strong>
<ul>
<li>
<p>Place a string of text (less than 20 characters) on top of the HuskyLens UI. The position of the texts (X,Y) coordinate is the top left of the text box.</p>
</li>
<li>
<p>You can have at most 10 custom texts on the UI at once, and if you continue adding texts you will replace previous texts in a circular fashion. For example, if you enter 10 texts you will fill the text buffer. If you then insert a new text object, you will overwrite the first text position (textBuffer[0]). Inserting another new text object will overwrite the second text position (textBuffer[1]).</p>
</li>
<li>
<p>Each text is uniquely identified by its (X,Y) coordinate, so you can replace the text string at a (X,Y) coordinate instead of adding a new text object. For example, if you insert “TEST_1” at (120,120) and then later submit “TEST_2” at (120,120), you will replace the string “TEST_1” with “TEST_2” and maintain an overall text count of 1.</p>
</li>
</ul>
</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd><code>"Text_Value"</code> :  (String) value for the desired text</dd>
<dd><code>X</code> :     (Integer) The X coordinate for the UI Object (0-320)</dd>
<dd><code>Y</code>:   (Integer) The Y coordinate for the UI Object (0-240)</dd>
</dl>
</dd>
<dd><strong>Returns:</strong>  Returns “Knock Received” on success<br>
<br></dd>
<dt>clearText()</dt>
<dd><strong>Description:</strong> Clear and delete all custom UI texts from the screen.</dd>
<dd><strong>Returns:</strong>  Returns “Knock Received” on success</dd>
</dl>
<h2 id="utility-functions">Utility Functions</h2>
<dl>
<dt>saveModelToSDCard( fileNum )</dt>
<dd><strong>Description:</strong> Save the current algorithms model file (its learned object data) to the SD Card. The file will be the in the format “AlgorithimName_Backup_<em>FileNum</em>.conf”</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd><code>fileNum</code> : (Integer) The specified file number to be used in the name for the file</dd>
</dl>
</dd>
<dd><strong>Returns:</strong>  Returns “Knock Received” on success. If there is no SD Card inserted or an SD Card Error, there will be a UI popup on the HuskyLens outlining the issue.<br>
<br></dd>
<dt>loadModelFromSDCard( fileNum )</dt>
<dd><strong>Description:</strong> Load a model file from the SD Card to the current algorithm and refresh the algorithm. The loaded file will be the following format “AlgorithimName_Backup_<em>FileNum</em>.conf”</dd>
<dd>
<dl>
<dt><strong>Arguments:</strong></dt>
<dd><code>fileNum</code> : (Integer) The specified file number to be used in the name for the file</dd>
</dl>
</dd>
<dd><strong>Returns:</strong>  Returns “Knock Received” on success. If there is no SD Card inserted or an SD Card Error, there will be a UI popup on the HuskyLens outlining the issue.<br>
<br></dd>
<dt>savePictureToSDCard( )</dt>
<dd><strong>Description:</strong> Save a photo from the HuskyLens camera onto the SD Card.</dd>
<dd><strong>Returns:</strong>  Returns “Knock Received” on success. If there is no SD Card inserted or an SD Card Error, there will be a UI popup on the HuskyLens outlining the issue.<br>
<br></dd>
<dt>saveScreenshotToSDCard( )</dt>
<dd><strong>Description:</strong> Save a screenshot of the HuskyLens UI onto the SD Card.</dd>
<dd><strong>Returns:</strong>  Returns “Knock Received” on success. If there is no SD Card inserted or an SD Card Error, there will be a UI popup on the HuskyLens outlining the issue.</dd>
</dl>
<br>
<hr>
