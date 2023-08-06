from datetime import datetime;
from . import Logger;
class DebugManager():
	def now(self):
  		return datetime.utcnow();
	def __init__(self):
		self.time = [];
		self.total_time = None;
		self.start_time = 0;

	def trace(self, name=''):
		time = self.time;
		time.append({
			'time': self.now(),
			'name': name
		});

	def show(self, name='Noname'):
		time = self.time;
		Logger.v('show trace for %s'%(name));
		for x in range(1, len(time)):
			Logger.v('\ttime spend on action %s : %s, %ss'%(x, time[x]['name'], time[x]['time'] - time[x-1]['time']));
		if(self.total_time):
			Logger.v('\t\t total time accumulated: %ss'%self.total_time);

	def start(self):
		self.start_time = self.now();

	def end(self):
		if(self.total_time):
			self.total_time += (self.now()-self.start_time);
		else:
			self.total_time = (self.now()-self.start_time);