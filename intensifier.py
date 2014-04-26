import sys
import random
import os, subprocess

################################################################################
# Configuration stuff
imFolder = 'D:/files/4/programs/terminal-utilities/imagemagick/'
im = imFolder + 'convert.exe'
id = imFolder + 'identify.exe'
tempFolder = 'temp/'

################################################################################
# Gets the dimensions of the input image
def getDimensions(filename):
  cmd = id + ' -format "%%w:%%h" "%s"' % filename
  print("Getting image information...")
  output = subprocess.check_output(cmd, shell=True)
  res = str(output)[2:-1].split(':')
  w = int(res[0])
  h = int(res[1])
  return w, h

################################################################################
# Generates shaken frames with optional subtitles
def generateFrames(filename, shift, frames, w, h, longestEdge, doSubtitle, subtitleText):
  wNew = w - (shift * 2) # size of resulting frame
  hNew = h - (shift * 2)

  subtitleFront = '( -size %dx%d -background none -gravity center ' % (wNew, shift * 5)
  subtitleFront += '-fill white -strokewidth 3 -font "Arial-Bold" -stroke '
  subtitleBack = ' label:"%s" ) -gravity south -composite ' % subtitleText

  print("Generating %d frames..." % frames)
  for i in range(frames):
    x = shift + random.randint(shift * -1, shift)
    y = shift + random.randint(shift * -1, shift)
    cmd = im + ' "%s" ' % filename
    cmd += '-crop %dx%d+%d+%d ' % (wNew, hNew, x, y)
    if doSubtitle:
      cmd += subtitleFront + "black" + subtitleBack
      cmd += subtitleFront + "none" + subtitleBack
    cmd += '-resize "%dx%d>" ' % (longestEdge, longestEdge)
    cmd += '%s%03d.jpg' % (tempFolder, i)
    os.system(cmd)

################################################################################
# Converts the generated frames into a GIF
def animate(filename, colors, delay):
  cmd = im + ' -delay %.1f -loop 0 -dispose none -colors %d ' % (delay, colors)
  cmd += '-coalesce %s*.jpg "%s.gif"' % (tempFolder, filename)
  print("Animating...")
  os.system(cmd)

################################################################################
# Main function, handles the other steps
def shake(filename, shiftPercent=2, frames=5, doSubtitle=False, subtitleText="", delay=1.5, longestEdge=500, colors=192):
  w, h = getDimensions(filename)
  shiftPixels = round((w + h) / 2 * shiftPercent / 100)
  print('Maximum shift is %d pixels. (%.1f%%)' % (shiftPixels, shiftPercent))
  generateFrames(filename, shiftPixels, frames, w, h, longestEdge, doSubtitle, subtitleText)
  animate(filename, colors, delay)
  print('Done.')
  os.system('"%s.gif"' % filename)

################################################################################
# Handle user arguments
def main():
  print()
  try:
    filename = sys.argv[1]
  except:
    filename = 'input.jpg'

  if '-doSubtitle' in sys.argv:
    print("What should the subtitle be?")
    subtitle = input()
    shake(filename, doSubtitle=True, subtitleText=subtitle)
  else:
    shake(filename)

################################################################################
# Program entrypoint
if __name__ == "__main__":
  main()
