import os
import asyncio
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import PIL.Image
import base64
import time
import math
import sys
import PIL.ImageFont
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

import argparse
import io
from google.cloud import vision
from PIL import Image, ImageDraw
import main


# Run Configuration
os.environ['COZMO_PROTOCOL_LOG_LEVEL'] = 'DEBUG'
os.environ['COZMO_LOG_LEVEL'] = 'DEBUG'
USE_VIEWER = True
USE_LOGGING = False
USE_FILTER = True
CUBE_SEARCH_TIMEOUT = 3
DISPLAY_TEXT_DURATION = 0.75
# Note: To use a custom font, uncomment the below line, set path/size, and restore font parameter on line 59.
# FONT = PIL.ImageFont.truetype("./fonts/Avenir-Roman.ttf", 24)
PURPLE = cozmo.lights.Color(rgb=(138, 43, 226 ))
GREEN = cozmo.lights.Color(rgb=(0, 255, 0))
ORANGE = cozmo.lights.Color(rgb=(255, 165, 0))

# Constants
FILTERED = frozenset(["black and white", "monochrome photography", "black", "white", "monochrome", "image", "photography"])

# Requires Google API Client Library for Python:
# pip3 install --upgrade google-api-python-client

'''
Google Cloud Vision Test
-Experimenting with Cozmo's camera and Google Cloud Vision API
-When you tap a cube, Cozmo says what he thinks he's seeing
-Certain results are filtered
-Images are saved as png files
-Note: Requires setting key file in environment variable GOOGLE_APPLICATION_CREDENTIALS

@author Team Cozplay
'''
class CloudVisionTest:
    def __init__(self):
        # self.startBoard = []
        self.startBoard = [["." for x in range(9)] for y in range(9)]
        self.solveList= []
        self._count = 0
        self._cube = 0
        self._cubes = [] #list of lists
        self._robot = None
        self._is_busy = False
        self.boardSide = 609.6;
        self.squareSide = 67.73;
        if USE_LOGGING:
            cozmo.setup_basic_logging()
        if USE_VIEWER:
            cozmo.connect_with_tkviewer(self.run)
        else:
            cozmo.connect(self.run)

    async def set_up_cozmo(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self._robot = await coz_conn.wait_for_robot()
        self._robot.camera.image_stream_enabled = True
        await self._robot.set_lift_height(1.0).wait_for_completed()
        await self._robot.set_head_angle(cozmo.util.Angle(degrees=0.0)).wait_for_completed()
        try:
            # target = await self._robot.world.wait_until_observe_num_objects(1, cozmo.objects.LightCube)
            # self._cubes.append(target)
            # self.boardSide = 2*(math.sqrt(((target[0].pose.position.x - self._robot.pose.position.x)**2)+((target[0].pose.position.y - self._robot.pose.position.y)**2)))
            # self.squareSide =  self.boardSide/9
            print("cube 1 = " + str(self.boardSide) + "\n")
            await self.readBoard()
        except TimeoutError:
            print("Could not find cube")
            return False

    async def readBoard(self):
        # for i in range(9):
        #     self.startBoard.append([])
        #     for x in range(9):
        #         self.startBoard[i].append(".")
        try:
            cubes = await self._robot.world.wait_until_observe_num_objects(1, cozmo.objects.LightCube)
            self._cube = cubes[0]
        except TimeoutError:
            print("Could not find cube")
            return False
        await self._robot.say_text("Let's do Sudoku", duration_scalar=1.2).wait_for_completed()
        self._cube.color = PURPLE
        await self._robot.drive_straight(distance_mm(-self.squareSide), speed_mmps(65)).wait_for_completed()
        self._robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, self.on_object_tapped)


    async def on_object_tapped(self, event, *, obj, tap_count, tap_duration, **kw):
        if self._is_busy:
            return
        else:
            # self._is_busy = True
            # self._cube.color = ORANGE
            # row = 8
            # col = 0
            # for i in range(9):
            #     response = await self.send_text_request()
            #     if response:
            #         value = await self.process_text_response(response)
            #         print(value)
            #         self.startBoard[row][col] = value[0]
            #     self._is_busy = False
            #     for x in range(8):
            #         row-=1
            #         await self._robot.drive_straight(distance_mm(self.squareSide), speed_mmps(90)).wait_for_completed()
            #         # await self._robot.set_lift_height(1.0).wait_for_completed()
            #         await self._robot.set_head_angle(cozmo.util.Angle(degrees=-25.0)).wait_for_completed()# changed fom 0
            #         response = await self.send_text_request()
            #         if response:
            #             value = await self.process_text_response(response)
            #             print(value)
            #             self.startBoard[row][col] = value[0]
            #         self._is_busy = False
            #     col += 1
            #     row = 8
            #     await self._robot.drive_straight(distance_mm(-8*self.squareSide + (2*(self.squareSide/3))), speed_mmps(195)).wait_for_completed()#Change for real board
            #     if i != 8:
            #         await self._robot.turn_in_place(degrees(-90)).wait_for_completed()
            #         await self._robot.drive_straight(distance_mm(self.squareSide), speed_mmps(90)).wait_for_completed()
            #         await self._robot.turn_in_place(degrees(90)).wait_for_completed()
            # await self._robot.turn_in_place(degrees(90)).wait_for_completed()
            # await self._robot.drive_straight(distance_mm(self.boardSide-(self.squareSide)), speed_mmps(195)).wait_for_completed()
            # await self._robot.turn_in_place(degrees(-90)).wait_for_completed()
            # await self._robot.drive_straight(distance_mm(self.squareSide), speed_mmps(90)).wait_for_completed()
            # s = ""
            # for row in range (0,9):
            #     for col in range(0,9):
            #         s+= self.startBoard[row][col]
            # f = open('board.txt', 'w')
            # f.write(s)
            # print(s)
            try:
                cubes = await self._robot.world.wait_until_observe_num_objects(1, cozmo.objects.LightCube)
                self._cube = cubes[0]
            except TimeoutError:
                print("Could not find cube")
                return False
            await self._robot.say_text("I've solved the puzzle", duration_scalar=1.2).wait_for_completed()
            self._cube.color = GREEN
            self._robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, self.solveBoard)


    async def solveBoard(self, event, *, obj, tap_count, tap_duration, **kw):
        main.main()
        g = open('solvelist.txt', 'r')
        lines = g.readlines()
        for line in lines:
            parts = line.split()
            square = (parts[0], parts[1], parts[2])
            self.solveList.append(square)
        if len(self.solveList)==0:
            await self._robot.say_text("I've tried my best, but this puzzle is unsolvable", duration_scalar=1.2).wait_for_completed()
            anim = await self.coz.play_anim('PeekABooGetOutSad').wait_for_completed()
            sys.exit()
            quit()
        start = (8,0)
        end = self.solveList[0]
        length = len(self.solveList)
        for x in range(1,length+1):
            s0 = int(start[0])
            s1 = int(start[1])
            e0 = int(end[0])
            e1 = int(end[1])
            w = abs(e1 - s1) * self.squareSide
            h = abs(e0 - s0)  * self.squareSide
            z = math.sqrt((h**2) + (w**2)) #diagonal line
            y = 0 #angle to turn
            k = 0 #angle to turn to get back to facing up
            #cases
            if s0>e0 and s1<e1: #up right
                y = -1*math.degrees(math.asin((w/z)))
                k = -1*(y)
            if s0>e0 and s1>e1: #up left
                y= math.degrees(math.asin((w/z)))
                k = -1*(y)
            if s0<e0 and s1<e1: #down right
                y= -1*(math.degrees(math.asin((h/z)))+90)
                k = -1*(y)
            if s0<e0 and s1>e1: # down left
                y= math.degrees(math.asin((h/z)))+90
                k = -1*(y)
            if s0==e0 and s1<e1: # straight right
                y= -90
                k = -1*(y)
            if s0==e0 and s1>e1: # straight left
                y=90
                k = -1*(y)
            if s0>e0 and s1==e1: # straight up
                y=0
                k=0
            if s0<e0 and s1==e1: # straight down
                y=180
                k = -1*(y)
            print("Y", str(y), "W", str(w), "H", str(h), "Z", str(z))
            await self._robot.turn_in_place(degrees(y)).wait_for_completed() #turn in correct direction
            await self._robot.drive_straight(distance_mm(z), speed_mmps(170)).wait_for_completed() #go correct distance
            await self._robot.turn_in_place(degrees(k)).wait_for_completed()
            await self._robot.say_text(str(end[2]), duration_scalar=1.2).wait_for_completed()

            start = end
            if x == length:
                break
            end = self.solveList[x]
        anim = await self.coz.play_anim('MajorWin').wait_for_completed()

    async def crop(self,filename):
        im = Image.open(filename)
        im2 = im.crop([80,60,240,180])
        print("crop")
        im2.save( "output_"+ filename, 'png')

    # Send an image label request using Cozmo's current camera image
    async def send_text_request(self):
        await self._robot.set_head_angle(cozmo.util.Angle(degrees=-25.0)).wait_for_completed()
        print("Text Request")
        cozmo_image = self._robot.world.latest_image
        if not cozmo_image:
            return None

        f = "vision_test_" + str(self._count) + "_" + str(time.time()) + ".png"
        cozmo_image.raw_image.save(f)
        self._count += 1

        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('vision', 'v1', credentials=credentials)
        await self.crop(f)
        with open("output_"+f, 'rb') as image:
            image_content = base64.b64encode(image.read())
            service_request = service.images().annotate(body={
                'requests': [{
                    'image': {
                        'content': image_content.decode('utf-8')
                    },
                    'features': [
                        {
                            'type': 'TEXT_DETECTION',
                            'maxResults': 1
                        }
                    ],
                    "imageContext": {
                        "languageHints": [
                            "ko"
                        ]
                    }
                }]
            })
        response = service_request.execute()
        return response

    # Cozmo says and shows the results
    async def process_text_response(self, response):
        self._cube.color = GREEN
        try:
            annotations = []
            for annotation in response['responses'][0]['textAnnotations']: #THINGY THERE
                if (not USE_FILTER) or (not FILTERED.__contains__(annotation['description'])):
                    annotations.append(annotation['description'])
        except KeyError:
            await self._robot.say_text("Blank", duration_scalar=1.2).wait_for_completed()
            return "."

        if len(annotations) == 0:
            pass
        else:
            await self._robot.say_text(annotations[0], duration_scalar=1.2).wait_for_completed()
            print(annotations[0])
            return annotations[0]
        await self._robot.set_lift_height(1.0).wait_for_completed()
        await self._robot.set_head_angle(cozmo.util.Angle(degrees=-25.0)).wait_for_completed()#changed from 0
        self._cube.color = PURPLE

    async def run(self, coz_conn):
        # Set up Cozmo
        await self.set_up_cozmo(coz_conn)

        while True:
            await asyncio.sleep(0)
        pass


class CloudVisionCube(cozmo.objects.LightCube):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._color = cozmo.lights.off

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: cozmo.lights.Color):
        self._color = value
        self.set_lights(cozmo.lights.Light(value))

if __name__ == '__main__':
    cozmo.world.World.light_cube_factory = CloudVisionCube
    CloudVisionTest()
