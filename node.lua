gl.setup(NATIVE_WIDTH, NATIVE_HEIGHT)

local rpc = require "rpc"
local py = rpc.create()

local detected_faces = {}

py.register("faces", function(faces)
   print("faces")
   detected_faces = faces

   -- {
   --    confidence = 62,
   --    marks = { { 168, 76 }, { 174, 75 }, { 178, 86 }, { 179, 100 }, { 182, 99 } },
   --    match = { 148, 51, 47, 64 }
   -- }

   pp(faces)
end)

local w = resource.create_colored_texture(1,1,1,1)

function node.render()
    for i, face in ipairs(detected_faces) do
        w:draw(
            face.match[1], 
            face.match[2], 
            face.match[1] + face.match[3], 
            face.match[2] + face.match[4]
        )
    end
end
