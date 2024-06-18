const ffmpeg = require('ffmpeg');
const concat = require('ffmpeg-concat');
//const fluent-ffmpeg = require('fluent-ffmpeg');

const fs = require('fs');
const path = require('path');

const outputVideo = '/home/carlos/ShortMaker/ffmpeg/final_video.mp4';
const folderPath = '/home/carlos/ShortMaker/ffmpeg/temp/';

// Function to retrieve all files in a directory recursively
function getAllFiles(dirPath, arrayOfFiles) {
  const files = fs.readdirSync(dirPath);

  arrayOfFiles = arrayOfFiles || [];

  files.forEach(file => {
    const filePath = path.join(dirPath, file);
    if (fs.statSync(filePath).isDirectory()) {
      arrayOfFiles = getAllFiles(filePath, arrayOfFiles);
    } else {
      arrayOfFiles.push(filePath);
    }
  });

  return arrayOfFiles;
}

// Get all files recursively from the ./temp directory
const allFiles = getAllFiles(folderPath);

console.log(allFiles)

const transitions = [
  {
    name: 'circleOpen',
    duration: 1000
  },
  {
    name: 'crossWarp',
    duration: 800
  },
  {
    name: 'directionalWarp',
    duration: 500,
    params: { direction: [1, -1] }
  },
  {
    name: 'squaresWire',
    duration: 2000
  }
];



// Function to create the final object
function createFinalObject(outputFileName, allFiles, transitions) {
  const finalObject = {
    output: outputFileName,
    videos: allFiles,
    transitions: []
  };

  // Iterate through allFiles and add transitions
  let transitionIndex = 0;
  for (let i = 1; i < allFiles.length; i++) {
    const transition = transitions[transitionIndex];
    finalObject.transitions.push(transition);
    transitionIndex = (transitionIndex + 1) % transitions.length;
  }

  return finalObject;
}

// Create the final object
const finalObject = createFinalObject("/home/carlos/ShortMaker/ffmpeg/final_video.mp4", allFiles, transitions);

concat(finalObject)


console.log("check for concatjs")

const { spawn } = require('child_process');

const scriptPath = '/home/carlos/ShortMaker/ffmpeg/script2.sh';

const child = spawn('bash', [scriptPath]);

child.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

child.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

child.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});

