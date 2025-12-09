'use client'

import SeismoMap from '@/components/SeismoMap'
import { useEffect, useState } from 'react'

export default function Home() {
	const [result, setResult] = useState(null)
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState(null)

	useEffect(() => {
		const fetchData = async () => {
			setLoading(true)
			try {
				const resp = await fetch('http://127.0.0.1:8000/process_server_files', {
					method: 'POST',
				})
				if (!resp.ok) throw new Error('Server error')
				const data = await resp.json()
				setResult(data)
			} catch (err) {
				setError(err.message)
			} finally {
				setLoading(false)
			}
		}

		fetchData()
	}, [])

	if (loading) return <p className='p-8'>Loading...</p>
	if (error) return <p className='p-8'>Error: {error}</p>
	if (!result) return <p className='p-8'>No data yet</p>

	return (
		<div className='p-8 space-y-6'>
			<h1 className='text-2xl font-bold'>Seismic Event Result</h1>

			<SeismoMap result={result} />
		</div>
	)
}
