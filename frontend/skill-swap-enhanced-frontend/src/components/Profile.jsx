import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'

const Profile = () => {
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <Card>
          <CardHeader>
            <CardTitle>User Profile</CardTitle>
            <CardDescription>View and edit your profile information</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">Profile component coming soon...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Profile

