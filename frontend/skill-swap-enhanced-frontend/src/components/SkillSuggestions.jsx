import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'

const SkillSuggestions = () => {
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <Card>
          <CardHeader>
            <CardTitle>Skill Suggestions</CardTitle>
            <CardDescription>Discover new skills based on your interests</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">Skill suggestions component coming soon...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default SkillSuggestions

