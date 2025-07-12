import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { Calendar, Users, BookOpen, Trophy, Clock, CheckCircle, X } from 'lucide-react'

const Dashboard = () => {
  // Mock data for demonstration
  const stats = [
    { icon: <Users className="h-5 w-5" />, label: 'Connections', value: '12' },
    { icon: <BookOpen className="h-5 w-5" />, label: 'Sessions', value: '8' },
    { icon: <Trophy className="h-5 w-5" />, label: 'Badge', value: 'Gold' },
    { icon: <Clock className="h-5 w-5" />, label: 'Hours', value: '24' }
  ]

  const pendingRequests = [
    {
      id: 1,
      name: 'Alex Johnson',
      skill: 'Python Programming',
      type: 'received',
      message: 'Hi! I\'d love to learn Python from you in exchange for teaching you photography.'
    },
    {
      id: 2,
      name: 'Maria Garcia',
      skill: 'Spanish Language',
      type: 'sent',
      message: 'Interested in learning Spanish? I can teach you in exchange for web development lessons.'
    }
  ]

  const upcomingSessions = [
    {
      id: 1,
      name: 'Sarah Chen',
      skill: 'UI/UX Design',
      date: '2024-01-15',
      time: '2:00 PM',
      type: 'learning'
    },
    {
      id: 2,
      name: 'Mike Rodriguez',
      skill: 'JavaScript',
      date: '2024-01-16',
      time: '10:00 AM',
      type: 'teaching'
    }
  ]

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome back! Here's what's happening with your skill exchanges.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {stats.map((stat, index) => (
            <Card key={index}>
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <div className="text-primary">{stat.icon}</div>
                  <div>
                    <p className="text-2xl font-bold">{stat.value}</p>
                    <p className="text-sm text-muted-foreground">{stat.label}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Pending Requests */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Pending Requests
              </CardTitle>
              <CardDescription>
                Manage your incoming and outgoing swap requests
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {pendingRequests.map((request) => (
                  <div key={request.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <Avatar className="h-8 w-8">
                          <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${request.name}`} />
                          <AvatarFallback>{request.name.charAt(0)}</AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="font-medium">{request.name}</p>
                          <p className="text-sm text-muted-foreground">{request.skill}</p>
                        </div>
                      </div>
                      <Badge variant={request.type === 'received' ? 'default' : 'secondary'}>
                        {request.type === 'received' ? 'Received' : 'Sent'}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mb-3">
                      {request.message}
                    </p>
                    {request.type === 'received' && (
                      <div className="flex gap-2">
                        <Button size="sm" className="flex-1">
                          <CheckCircle className="h-4 w-4 mr-2" />
                          Accept
                        </Button>
                        <Button size="sm" variant="outline" className="flex-1">
                          <X className="h-4 w-4 mr-2" />
                          Decline
                        </Button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Upcoming Sessions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Upcoming Sessions
              </CardTitle>
              <CardDescription>
                Your scheduled learning and teaching sessions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {upcomingSessions.map((session) => (
                  <div key={session.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <Avatar className="h-8 w-8">
                          <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${session.name}`} />
                          <AvatarFallback>{session.name.charAt(0)}</AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="font-medium">{session.name}</p>
                          <p className="text-sm text-muted-foreground">{session.skill}</p>
                        </div>
                      </div>
                      <Badge variant={session.type === 'learning' ? 'default' : 'secondary'}>
                        {session.type === 'learning' ? 'Learning' : 'Teaching'}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground mb-3">
                      <span>{session.date}</span>
                      <span>{session.time}</span>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" className="flex-1">
                        Join Session
                      </Button>
                      <Button size="sm" variant="ghost">
                        Reschedule
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>
              Common tasks to help you get started
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                <Users className="h-6 w-6" />
                <span>Browse Users</span>
              </Button>
              <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                <Calendar className="h-6 w-6" />
                <span>Schedule Session</span>
              </Button>
              <Button variant="outline" className="h-auto p-4 flex flex-col items-center gap-2">
                <Trophy className="h-6 w-6" />
                <span>View Leaderboard</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard

