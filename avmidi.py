import ctypes
import time
from objc_util import *

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioUnitSampler = ObjCClass('AVAudioUnitSampler')
AVAudioSession = ObjCClass('AVAudioSession')

def setup():
    error = ctypes.c_void_p(0)
    session = AVAudioSession.sharedInstance()
    category = session.setCategory('AVAudioSessionCategoryPlayAndRecord', error=ctypes.pointer(error))
    if error:
        raise Exception('error setting up category')
    session.setActive(True, error=ctypes.pointer(error))
    if error:
        raise Exception('error setting up session active')
    engine = AVAudioEngine.new()
    return engine

engine = setup()
sampler = AVAudioUnitSampler.new()
engine.attachNode(sampler)
engine.connect_to_format_(sampler, engine.mainMixerNode(), None)
engine.startAndReturnError_(None)

error = ctypes.c_void_p(0)
sampler.loadSoundBankInstrumentAtURL_program_bankMSB_bankLSB_error_(nsurl('./fluid.sf2'), 0, 0x79, 0, ctypes.pointer(error))
if error:
    print('Error loading sound bank')
sampler.startNote_withVelocity_onChannel_(60, 80, 0)
time.sleep(8)
sampler.stopNote_onChannel_(60, 0)

print('success')
