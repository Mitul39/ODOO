import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { Textarea } from './ui/textarea'

const CreateProfile = () => {
  const [formData, setFormData] = useState({
    bio: '',
    skillsOffered: '',
    skillsWanted: '',
    availability: '',
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    // TODO: Implement profile creation
    console.log('Profile data:', formData)
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-2xl">
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Create Your Profile</CardTitle>
            <CardDescription>
              Tell us about yourself and the skills you want to share and learn
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="bio">Bio</Label>
                <Textarea
                  id="bio"
                  name="bio"
                  placeholder="Tell us about yourself..."
                  value={formData.bio}
                  onChange={handleChange}
                  rows={4}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="skillsOffered">Skills You Can Teach</Label>
                <Input
                  id="skillsOffered"
                  name="skillsOffered"
                  placeholder="e.g., Python, Cooking, Guitar"
                  value={formData.skillsOffered}
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="skillsWanted">Skills You Want to Learn</Label>
                <Input
                  id="skillsWanted"
                  name="skillsWanted"
                  placeholder="e.g., Photography, Spanish, Marketing"
                  value={formData.skillsWanted}
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="availability">Availability</Label>
                <Input
                  id="availability"
                  name="availability"
                  placeholder="e.g., Weekends, Evenings"
                  value={formData.availability}
                  onChange={handleChange}
                />
              </div>

              <Button type="submit" className="w-full">
                Create Profile
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default CreateProfile

