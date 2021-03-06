import ctypes
from objc_util import ObjCClass, nsurl
from pathlib import Path


def getDefaultSoundBank():
    soundBankFolder = Path(__file__).parent / 'SoundBanks'
    for sb in soundBankFolder.glob('*.sf2'):
        return str(soundBankFolder / sb)


def convertNote(note):
    if isinstance(note, int):
        return note
    if not isinstance(note, str):
        raise Exception(f'Invalid note {note}')
    mappedNote = _noteMap.get(note.lower())
    if mappedNote is None:
        raise Exception(f'Invalid note {note}')    
    return mappedNote


class MIDIInstrument:
    def __init__(self, soundBank=None, instrument=0):
        self._engine = self._setupEngine()
        self._sampler = self._setupSampler(self._engine)
        self._engine.startAndReturnError_(None)
        self._soundBank = soundBank if soundBank else getDefaultSoundBank()
        self.loadInstrument(instrument)
        
    def loadInstrument(self, instrument):
        if self._soundBank is None:
            return
        error = ctypes.c_void_p(0)
        self._sampler.loadSoundBankInstrumentAtURL_program_bankMSB_bankLSB_error_(nsurl(self._soundBank), instrument, 0x79, 0, ctypes.pointer(error))
        if error:
            raise Exception(f'Error loading sound bank {self._soundBank}')
            
    def playNote(self, note, velocity=80):
        self._sampler.startNote_withVelocity_onChannel_(convertNote(note), velocity, 0)

    def stopNote(self, note):
        self._sampler.stopNote_onChannel_(convertNote(note), 0)

    def _setupEngine(self):
        AVAudioEngine = ObjCClass('AVAudioEngine')
        AVAudioSession = ObjCClass('AVAudioSession')
        error = ctypes.c_void_p(0)
        session = AVAudioSession.sharedInstance()
        category = session.setCategory('AVAudioSessionCategoryPlayback', error=ctypes.pointer(error))
        if error:
            raise Exception('error setting up category')
        session.setActive(True, error=ctypes.pointer(error))
        if error:
            raise Exception('error setting up session active')
        engine = AVAudioEngine.new()
        return engine      

    def _setupSampler(self, engine):
        AVAudioUnitSampler = ObjCClass('AVAudioUnitSampler')
        sampler = AVAudioUnitSampler.new()
        engine.attachNode(sampler)
        engine.connect_to_format_(sampler, engine.mainMixerNode(), None)
        return sampler

def _buildNoteMap():
    noteMap = {}
    octave = ['c{}', 'c{}#', 'd{}', 'd{}#', 'e{}', 'f{}', 'f{}#', 'g{}', 'g{}#', 'a{}', 'a{}#', 'b{}']
    midiNote = 24
    for o in range(1, 8):
        for n in octave:
            noteMap[n.format(o)] = midiNote
            midiNote += 1
    return noteMap


_noteMap = _buildNoteMap()
