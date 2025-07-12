import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Badge } from './ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { Search, Star, MessageCircle } from 'lucide-react'

const BrowseUsers = () => {
  const [searchTerm, setSearchTerm] = useState('')

  // Mock data for demonstration
  const users = [
    {
      id: 1,
      name: 'Sarah Chen',
      bio: 'UX Designer with 5 years of experience',
      skillsOffered: ['UI/UX Design', 'Figma', 'User Research'],
      skillsWanted: ['Python', 'Data Analysis'],
      badge: 'Gold',
      rating: 4.8,
      sessionsCompleted: 23
    },
    {
      id: 2,
      name: 'Mike Rodriguez',
      bio: 'Full-stack developer and coding mentor',
      skillsOffered: ['JavaScript', 'React', 'Node.js'],
      skillsWanted: ['Machine Learning', 'DevOps'],
      badge: 'Platinum',
      rating: 4.9,
      sessionsCompleted: 45
    },
    {
      id: 3,
      name: 'Emma Thompson',
      bio: 'Digital marketing specialist',
      skillsOffered: ['SEO', 'Content Marketing', 'Social Media'],
      skillsWanted: ['Graphic Design', 'Video Editing'],
      badge: 'Silver',
      rating: 4.7,
      sessionsCompleted: 18
    }
  ]

  const getBadgeColor = (badgeLevel) => {
    switch (badgeLevel) {
      case 'Bronze': return 'badge-bronze'
      case 'Silver': return 'badge-silver'
      case 'Gold': return 'badge-gold'
      case 'Platinum': return 'badge-platinum'
      default: return 'bg-gray-500'
    }
  }

  const filteredUsers = users.filter(user =>
    user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.skillsOffered.some(skill => skill.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-4">Browse Users</h1>
          <p className="text-muted-foreground mb-6">
            Find skilled individuals ready to share their knowledge
          </p>
          
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by name or skill..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredUsers.map((user) => (
            <Card key={user.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <Avatar className="h-12 w-12">
                    <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.name}`} />
                    <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{user.name}</CardTitle>
                      <Badge className={getBadgeColor(user.badge)}>
                        {user.badge}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2 mt-1">
                      <div className="flex items-center">
                        <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        <span className="text-sm text-muted-foreground ml-1">
                          {user.rating}
                        </span>
                      </div>
                      <span className="text-sm text-muted-foreground">
                        • {user.sessionsCompleted} sessions
                      </span>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-4">
                  {user.bio}
                </CardDescription>
                
                <div className="space-y-3">
                  <div>
                    <h4 className="text-sm font-medium mb-2">Can teach:</h4>
                    <div className="flex flex-wrap gap-1">
                      {user.skillsOffered.map((skill, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-medium mb-2">Wants to learn:</h4>
                    <div className="flex flex-wrap gap-1">
                      {user.skillsWanted.map((skill, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2 mt-4">
                  <Button size="sm" className="flex-1">
                    <MessageCircle className="h-4 w-4 mr-2" />
                    Request Swap
                  </Button>
                  <Button size="sm" variant="outline">
                    View Profile
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredUsers.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">No users found matching your search.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default BrowseUsers

